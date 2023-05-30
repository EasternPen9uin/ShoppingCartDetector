from PIL import Image
import os
###########################
# 이미지 원본파일이 저장된 폴더(폴더 안에 이미지 파일만 넣어야 합니다)
IMAGE_FOLDER = "shoppingcart"
# .jpg파일로 변환된 파일이 저장될 폴더
CONVERTED_IMAGES_FOLDER = "IMAGES_JPG"
###########################
def convert_to_jpg(filepath, folder):
    im = Image.open(filepath).convert('RGB')
    im.save(folder+"\\"+filepath.split('\\')[-1].split('.')[0]+'.jpg', 'JPEG')

def convertAFolderToJPG (input_folder, output_folder):
    for i in os.listdir(input_folder):
        if i == "desktop.ini":
            continue
        convert_to_jpg(input_folder+"\\"+i, output_folder)

############################
if CONVERTED_IMAGES_FOLDER not in os.listdir():
    os.system("mkdir " + CONVERTED_IMAGES_FOLDER)
convertAFolderToJPG(IMAGE_FOLDER, CONVERTED_IMAGES_FOLDER)
input("완료!")
