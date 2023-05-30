import os
###########################
# 이미지 원본파일이 저장된 폴더(폴더 안에 JPG 이미지 파일만 넣어야 합니다)
IMAGE_FOLDER = "nonshoppingcart"
# .jpg파일로 변환된 파일이 저장될 폴더
LABEL_FOLDER = "nonshoppingcart_label"
############################
if LABEL_FOLDER not in os.listdir():
    os.system("mkdir " + LABEL_FOLDER)

for i in os.listdir(IMAGE_FOLDER):
    if i.split('.')[-1] == 'jpg':
        f= open(LABEL_FOLDER+'/'+i.replace('.jpg','.txt'), 'w')
        f.close()
input("완료!")
