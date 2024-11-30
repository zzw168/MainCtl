import glob
import os
import shutil


def is_image_file(file_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    return os.path.splitext(file_path)[1].lower() in image_extensions



def getbackground(imgdir):

    img_list = glob.glob('%s/*.*' % imgdir)

    for img_path in img_list:

        if is_image_file(img_path):


            is_save = False

            file_name = os.path.basename(img_path)

            file_name_without_extension = os.path.splitext(file_name)[0]

            txta = imgdir+"/"+file_name_without_extension+".txt"

            if os.path.exists(txta):
                # 打开文件
                with open(txta, 'r') as file:
                    # 读取文件内容
                    file_content = file.read()

                    if len(file_content.translate(str.maketrans('', '', ' \n\t\r'))) == 0:
                        is_save = True

            else:
                is_save = True

            if is_save :
                # shutil.copyfile(img_path, "./background/" + file_name)
                shutil.move(img_path, "./background/" + file_name)




if __name__ == '__main__':

    getbackground(r'C:\Users\Administrator\Desktop\tr\auto_img_aicode\img')