import os
import cv2

def image_queue_worker(image_queue):
    while True:
        # 从队列中获取图片数据
        save_path,image_name,image_data = image_queue.get()

        if os.path.exists(save_path):

            # 使用 cv2.imencode 先将图像编码为 jpg 格式
            is_success, encoded_image = cv2.imencode('.jpg', image_data)

            # 如果编码成功
            if is_success:
                # 使用 open() 以二进制写入模式 ('wb') 保存文件
                with open(save_path+image_name, 'wb') as f:
                    f.write(encoded_image.tobytes())

        else:
            print(f"硬盘地址 {save_path} 不存在")

        image_queue.task_done()

