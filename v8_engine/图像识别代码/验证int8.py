import os
import argparse
from os import getcwd
import glob
from xml.etree import ElementTree as ET

from PIL import Image

from utils.general import *
# from utils.datasets import *
from utils import torch_utils
from ultralytics import YOLO  # YOLOV8
import shutil

import python_trt as myTr


# 定义一个创建一级分支object的函数
def create_object(root, xyxy, names, cls):  # 参数依次，树根，xmin，ymin，xmax，ymax
    # 创建一级分支object
    _object = ET.SubElement(root, 'object')
    # 创建二级分支
    name = ET.SubElement(_object, 'name')
    # print(obj_name)
    name.text = str(names[int(cls)])
    pose = ET.SubElement(_object, 'pose')
    pose.text = 'Unspecified'
    truncated = ET.SubElement(_object, 'truncated')
    truncated.text = '0'
    difficult = ET.SubElement(_object, 'difficult')
    difficult.text = '0'
    # 创建bndbox
    bndbox = ET.SubElement(_object, 'bndbox')
    xmin = ET.SubElement(bndbox, 'xmin')
    xmin.text = '%s' % int(xyxy[0])
    ymin = ET.SubElement(bndbox, 'ymin')
    ymin.text = '%s' % int(xyxy[1])
    xmax = ET.SubElement(bndbox, 'xmax')
    xmax.text = '%s' % int(xyxy[2])
    ymax = ET.SubElement(bndbox, 'ymax')
    ymax.text = '%s' % int(xyxy[3])


# 创建xml文件的函数
def create_tree(image_path, h, w):
    # 创建树根annotation
    annotation = ET.Element('annotation')
    # 创建一级分支folder
    folder = ET.SubElement(annotation, 'folder')
    # 添加folder标签内容
    folder.text = os.path.dirname(image_path)

    # 创建一级分支filename
    filename = ET.SubElement(annotation, 'filename')
    filename.text = os.path.basename(image_path)

    # 创建一级分支path
    path = ET.SubElement(annotation, 'path')

    path.text = image_path  # 用于返回当前工作目录getcwd() + '\{}'.format

    # 创建一级分支source
    source = ET.SubElement(annotation, 'source')
    # 创建source下的二级分支database
    database = ET.SubElement(source, 'database')
    database.text = 'Unknown'

    # 创建一级分支size
    size = ET.SubElement(annotation, 'size')
    # 创建size下的二级分支图像的宽、高及depth
    width = ET.SubElement(size, 'width')
    width.text = str(w)
    height = ET.SubElement(size, 'height')
    height.text = str(h)
    depth = ET.SubElement(size, 'depth')
    depth.text = '3'

    # 创建一级分支segmented
    segmented = ET.SubElement(annotation, 'segmented')
    segmented.text = '0'

    return annotation


def pretty_xml(element, indent, newline, level=0):  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素
        if (element.text is None) or element.text.isspace():  # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
            # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
            # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element)  # 将element转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        pretty_xml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作









def compute_iou(box1, box2):
    """
    计算两个边界框之间的IoU
    """
    x1, y1, x2, y2 = box1
    x1_, y1_, x2_, y2_ = box2

    xi1, yi1 = max(x1, x1_), max(y1, y1_)
    xi2, yi2 = min(x2, x2_), min(y2, y2_)
    inter_area = max(0, xi2 - xi1 + 1) * max(0, yi2 - yi1 + 1)

    box1_area = (x2 - x1 + 1) * (y2 - y1 + 1)
    box2_area = (x2_ - x1_ + 1) * (y2_ - y1_ + 1)
    union_area = box1_area + box2_area - inter_area

    iou = inter_area / union_area
    return iou


def filter_boxes(results, iou_threshold):
    """
    过滤不同类别的重叠框
    """
    boxes = results.boxes.xyxy.cpu().numpy()
    scores = results.boxes.conf.cpu().numpy()
    classes = results.boxes.cls.cpu().numpy()

    filtered_boxes = []
    for i in range(len(boxes)):
        box1 = boxes[i]
        class1 = classes[i]
        keep = True
        for j in range(len(boxes)):
            if i == j:
                continue
            box2 = boxes[j]
            class2 = classes[j]
            if class1 != class2 and compute_iou(box1, box2) > iou_threshold:
                if scores[i] < scores[j]:
                    keep = False
                    break
        if keep:
            filtered_boxes.append((box1, scores[i], class1))

    return filtered_boxes




def convert_to_normalized(box, img_width, img_height):
    """
    将边界框坐标转换为归一化数据
    """
    x1, y1, x2, y2 = box
    x_center = (x1 + x2) / 2.0 / img_width
    y_center = (y1 + y2) / 2.0 / img_height
    width = (x2 - x1) / img_width
    height = (y2 - y1) / img_height
    return x_center, y_center, width, height





def is_image_file(file_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    return os.path.splitext(file_path)[1].lower() in image_extensions













def compute_iou(box1, box2):
    """计算两个框之间的IoU"""
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2

    # 计算交集
    inter_x_min = max(x1_min, x2_min)
    inter_y_min = max(y1_min, y2_min)
    inter_x_max = min(x1_max, x2_max)
    inter_y_max = min(y1_max, y2_max)

    inter_area = max(0, inter_x_max - inter_x_min) * max(0, inter_y_max - inter_y_min)

    # 计算各自的面积
    box1_area = (x1_max - x1_min) * (y1_max - y1_min)
    box2_area = (x2_max - x2_min) * (y2_max - y2_min)

    # 计算并集
    union_area = box1_area + box2_area - inter_area

    # 计算IoU
    iou = inter_area / union_area
    return iou


def non_max_suppression(predictions, iou_threshold):
    """基于IoU阈值的非极大值抑制"""
    filtered_predictions = []

    # 对预测结果按置信度排序
    predictions = sorted(predictions, key=lambda x: x[1], reverse=True)

    while predictions:
        best_prediction = predictions.pop(0)
        filtered_predictions.append(best_prediction)

        predictions = [
            pred for pred in predictions
            if compute_iou(best_prediction[0], pred[0]) < iou_threshold
        ]

    return filtered_predictions


def Auto_label(weight, imgdir, yolo_txt_dir, label_baocun, label_nobiaoji, label_conf):
    # load model
    # model = YOLO(weight)


    img_list = glob.glob('%s/*.*' % imgdir)


    model = myTr.Detector(model_path=b"int8.engine", dll_path=r"yolov8.dll")

    # 正式

    for img_path in img_list:

        if is_image_file(img_path):

            img = Image.open(img_path)
            img_width, img_height = img.size

            aaimgsz = img_width
            if aaimgsz < 1280:
                aaimgsz = 1280


            # [(array([       1599,      756.37,      1644.8,      803.78], dtype=float32), 0.9033691, 2.0)]
            result = model.predict(img)
            results2 = model.visualize(result)

            print(results2)

            # 目标转换
            results = [
                (np.array(item[:4], dtype=np.float32), item[5], item[4])
                for item in results2
            ]


            # # 自定义IoU阈值
            # iou_threshold = 0.6
            #
            # # 过滤不同类别的重叠框
            # filtered_boxes = filter_boxes(results, iou_threshold)

            iou_threshold = 0.6
            filtered_predictions = non_max_suppression(results, iou_threshold)




            filtered_boxes = filtered_predictions


            # print("\n\n\n\n")
            #
            # print(filtered_boxes)
            # exit()

            yolo_data = []
            # 打印过滤后的框
            for box, score, cls in filtered_boxes:

                normalized_box = convert_to_normalized(box, img_width, img_height)

                # print(f"Box: {box}, Score: {score}, Class: {cls}")

                yolo_data.append(f"{int(cls)} {normalized_box[0]} {normalized_box[1]} {normalized_box[2]} {normalized_box[3]}")



            # Write YOLO format annotations to txt file
            txt_file_path = img_path.split('.')
            txt_file_path = txt_file_path[0].replace(imgdir, yolo_txt_dir)
            txt_file_path = '%s%s' % (txt_file_path, '.txt')
            # txt_file_path = img_path.replace(imgdir, yolo_txt_dir).replace('.png', '.txt')

            if len(yolo_data) > 0:


                # mv_jpg = txt_file_path.replace('.txt', '.jpg')
                # shutil.copyfile(img_path, mv_jpg)

                with open(txt_file_path, 'w') as f:
                    f.write('\n'.join(yolo_data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-text', type=str, default='img')
    parser.add_argument('-str', type=str, default='txt')
    parser.add_argument('-conf', type=float, default=0.5)
    args = parser.parse_args()
    print(args.text)

    # 加载模型
    weight_path = "./best.pt"  # 模型路径
    imgdir = args.text  # 图片路径
    txtdir = args.str  # 标注文件保存路径
    label_conf = args.conf
    print("图片路径:" + imgdir)
    print("标注路径:" + txtdir)
    print("conf:" + str(args.conf))

    label_baocun = ['yellow', 'blue', 'red', 'purple', 'orange', 'green', 'Brown', 'black', 'pink',
                    'White']  # 图片没有出现指定标签，删除
    label_nobiaoji = ['xx_s_yellow', 'xx_s_blue', 'xx_s_red', 'xx_s_purple', 'xx_s_orange', 'xx_s_green', 'xx_s_Brown',
                      'xx_s_black', 'xx_s_pink', 'xx_s_White']  # 指定标签不自动标记

    Auto_label(weight_path, imgdir, txtdir, label_baocun, label_nobiaoji, label_conf)  # 调用自标注函数
