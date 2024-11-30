#! /usr/bin/env python3
import json
import os
import pathlib
from datetime import datetime

import cv2 as cv
import numpy as np
import onnxruntime
from ultralytics import YOLO
import tensorrt as trt
from tqdm import tqdm

from polygraphy.backend.trt import NetworkFromOnnxPath, CreateConfig, EngineFromNetwork
from polygraphy.backend.trt import Calibrator


def _yolo8_2_onnx(pt_model_path):
    pt_model_path = pathlib.Path(pt_model_path).expanduser().resolve()
    if not pt_model_path.exists():
        raise FileNotFoundError(f'Model not found: {pt_model_path}')
    print(f'{pt_model_path= }')
    model = YOLO(pt_model_path)

    model.export(format='onnx')
    onnx_model_name = pt_model_path.stem + '.onnx'
    onnx_model = pt_model_path.parent / onnx_model_name
    print(f'Done! Model is exported as {onnx_model}')


def _get_metadata():
    description = f'Ultralytics YOLOv8X model'
    names = {
  "0": "yellow",
  "1": "blue",
  "2": "red",
  "3": "purple",
  "4": "orange",
  "5": "green",
  "6": "Brown",
  "7": "black",
  "8": "pink",
  "9": "White"
}  # 各个检测类别索引和名字的对应关系
    metadata = {
        'description': description,
        'author': 'Ultralytics',
        'license': 'AGPL-3.0 https://ultralytics.com/license',
        'date': datetime.now().isoformat(),
        'version': '8.0.186',
        'stride': 32,
        'task': 'detect',
        'batch': 1,
        'imgsz': [1504, 1504],
        'names': names
    }
    return metadata


def _calib_data_yolo8(onnx_input_name, onnx_input_shape,
                      calibration_images_quantity, calibration_images_folder):
    print(f' {onnx_input_shape= }')  #
    if onnx_input_shape[1] != 3:  
        raise ValueError(f'Error, expected input depth is 3, '
                         f'but {onnx_input_shape= }')
    calibration_images_folder = pathlib.Path(calibration_images_folder).expanduser().resolve()
    if not calibration_images_folder.exists():
        raise FileNotFoundError(f'{calibration_images_folder} does not exist.')
    print(f'{calibration_images_folder= }')

    batch_size = onnx_input_shape[0]
    required_height = onnx_input_shape[2]
    required_width = onnx_input_shape[3]
    output_images = np.zeros(shape=onnx_input_shape, dtype=np.float32)

    calibration_images_quantity = min(calibration_images_quantity,
                                      len(os.listdir(calibration_images_folder)))
    print(f'Calibration images quantity: {calibration_images_quantity}')
    print(f'Calibrating ...')
    tqdm_images_folder = tqdm(calibration_images_folder.iterdir(),
                              total=calibration_images_quantity, ncols=80)
    for i, one_image_path in enumerate(tqdm_images_folder):
        if i == calibration_images_quantity:
            break
        bgr_image = cv.imread(str(one_image_path))  # noqa
        bgr_image = cv.resize(bgr_image, (required_width, required_height))  # noqa
        one_rgb_image = bgr_image[..., ::-1]  # 

        one_image = one_rgb_image / 255  
        one_image = one_image.transpose(2, 0, 1)  

        batch_index = i % batch_size  
        output_images[batch_index] = one_image  
        if batch_index == (batch_size - 1):  
            one_batch_data = {onnx_input_name: output_images}
            yield one_batch_data  # 
            output_images = np.zeros_like(output_images)  


def onnx_2_trt_by_polygraphy(onnx_file, optimization_level=5,
                             conversion_target='int8', engine_suffix='engine',
                             calibration_method='min-max', calibration_images_quantity=64,
                             calibration_images_folder=None,
                             onnx_input_shape=None):

    if conversion_target.lower() not in ['int8', 'fp16', 'fp32']:
        raise ValueError(f"The conversion_target must be one of ['int8', 'fp16', 'fp32'], "
                         f"but get {conversion_target= }")
    if engine_suffix not in ['plan', 'engine', 'trt']:
        raise ValueError(f"The engine_suffix must be one of ['plan', 'engine', 'trt'], "
                         f"but get {engine_suffix= }")
    onnx_file = pathlib.Path(onnx_file).expanduser().resolve()
    if not onnx_file.exists():
        raise FileNotFoundError(f'Onnx file not found: {onnx_file}')
    print(f"Succeeded finding ONNX file! {onnx_file= }")

    print(f'Polygraphy inspecting model:')
    os.system(f"polygraphy inspect model {onnx_file}")  

    network = NetworkFromOnnxPath(str(onnx_file))  

    builder_config = CreateConfig(builder_optimization_level=optimization_level)
    print(f'{builder_config.builder_optimization_level= }')

    converted_trt_name = (f"{onnx_file.stem}_optimization_level_{optimization_level}"
                          f"_{conversion_target}")
    if conversion_target.lower() == 'fp16':
        builder_config.fp16 = True
        print(f'{builder_config.fp16= }')
    elif conversion_target.lower() == 'int8':

        builder_config.int8 = True
        print(f'{builder_config.int8= }')

        session = onnxruntime.InferenceSession(onnx_file, providers=['CPUExecutionProvider'])
        onnx_input_name = session.get_inputs()[0].name
        if onnx_input_shape is None:  
            onnx_input_shape = session.get_inputs()[0].shape


        calibration_cache_file = f"./{onnx_file.stem}_int8.cache"
        calibration_cache_file = pathlib.Path(calibration_cache_file).expanduser().resolve()
        if calibration_cache_file.exists():  
            os.remove(calibration_cache_file)

        if calibration_method == 'min-max':
            calibrator_class = trt.IInt8MinMaxCalibrator
        else:
            calibrator_class = trt.IInt8EntropyCalibrator2
        builder_config.calibrator = Calibrator(
            BaseClass=calibrator_class,
            data_loader=_calib_data_yolo8(onnx_input_name=onnx_input_name, onnx_input_shape=onnx_input_shape,
                                          calibration_images_quantity=calibration_images_quantity,
                                          calibration_images_folder=calibration_images_folder),
            cache=calibration_cache_file)
        int8_suffix = f'_{calibration_method}_images{calibration_images_quantity}'
        converted_trt_name = converted_trt_name + int8_suffix

    converted_trt = onnx_file.parent / (converted_trt_name + f'.{engine_suffix}')

    print('Building the engine ...')
    build_engine = EngineFromNetwork(network, config=builder_config)

    with build_engine() as engine, open(converted_trt, 'wb') as t:
        # 不跑评估需要注释
        # yolo8_metadata = _get_metadata()  
        # meta = json.dumps(yolo8_metadata)  

        # t.write(len(meta).to_bytes(4, byteorder='little', signed=True))
        # t.write(meta.encode())
        t.write(engine.serialize())

    engine_saved = ''
    if not pathlib.Path(converted_trt).exists():
        engine_saved = 'not '
    print(f'Done! {converted_trt} is {engine_saved.upper()}saved.')
    return str(converted_trt)


def validate_model(model_path, conf, iou, imgsz, dataset_split, agnostic_nms,
                   batch_size=1, simplify_names=True, **kwargs):

    model_path = pathlib.Path(model_path).expanduser().resolve()
    if not model_path.exists():
        raise FileNotFoundError(f'Model not found: {model_path}')
    print(f'{model_path= }')
    print(f'{conf= }, {iou= }, {imgsz= }')

    model = YOLO(model_path, task='detect')  

    detect_data = r'val_test.yaml'  # 校验数据集的配置文件

    if (model_path.suffix == '.pt') and simplify_names:
        model.names[0] = 'foo'  
        model.names[1] = 'bar'
    metrics = model.val(split=dataset_split, save=False,
                        data=detect_data,
                        agnostic_nms=agnostic_nms, batch=batch_size,
                        conf=conf, iou=iou, imgsz=imgsz,
                        **kwargs)
    map50 = round(metrics.box.map50, 3)
    print(f'{dataset_split} mAP50= {map50}')


def main():


    onnx_file = (r'best.transd.onnx')
    calibration_images =100
    calibration_images_folder = r'images'
    saved_engine = onnx_2_trt_by_polygraphy(
        onnx_file=onnx_file, optimization_level=5, conversion_target='int8',
        engine_suffix='engine', calibration_images_quantity=calibration_images,
        calibration_images_folder=calibration_images_folder)

    # 评估
    # saved_engine = r"best.pt"
    # saved_engine = r"best_optimization_level_5_int8_min-max_images1295.engine"
    #
    # validate_model(model_path=saved_engine,

    #                dataset_split='val_test',
    #                imgsz=1920,
    #                conf=0.45, iou=0.6, agnostic_nms=True)



if __name__ == '__main__':
    main()



# Model summary (fused): 218 layers, 25,847,866 parameters, 0 gradients, 78.7 GFLOPs
# val: Scanning C:\Users\Administrator\Desktop\tr\imga\val.cache... 403 images, 21 backgrounds, 0 corrupt: 100%|██████████| 403/403 [00:00<?, ?it/s]
#                  Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100%|██████████| 403/403 [00:30<00:00, 13.39it/s]
#                    all        403        564       0.98      0.983      0.988      0.918
#                 yellow         56         56      0.982          1      0.994       0.93
#                   blue         64         64      0.984      0.953      0.974       0.89
#                    red         29         29      0.933      0.966      0.981      0.943
#                 purple         77         77      0.921          1       0.99      0.894
#                 orange         60         60      0.993      0.967      0.983      0.921
#                  green         33         33          1          1      0.995      0.938
#                  Brown         46         46          1          1      0.995       0.95
#                  black         74         74      0.989      0.959      0.977      0.873
#                   pink         62         62          1          1      0.995      0.943
#                  White         63         63          1      0.984      0.991      0.901
# Speed: 1.5ms preprocess, 64.1ms inference, 0.0ms loss, 2.4ms postprocess per image0
# Results saved to runs\detect\val7
# val_test mAP50= 0.988



# Process finished with exit code 0


