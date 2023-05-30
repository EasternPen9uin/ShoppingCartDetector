# author : EasternPen9uin
# 이 프로그램은 YOLO방식 라벨링이 된 이미지(오직 jpg만)를
# 현상유지 + [좌우반전, 상하반전, 회전, 블러, 확대 , 왜곡] 중
# n개를 랜덤하게 선택하여 이미지를 증강합니다.
# 폴더 단위로만 선택 가능합니다.
######
import os
import numpy as np
import imageio
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
from imgaug import augmenters as iaa
import cv2
import random
#######
# 이미지 경로와 바운딩 박스 파일 경로 설정
input_path = 'test_shoppingcart' #폴더 이름
REPEAT = 6
output_path = input_path+'_augmented' #폴더 이름

########
if input(f"진짜로 실행합니까? (현재 대상 폴더 : {input_path} -> {output_path}) (Y/N)>>") != "Y":
    a= 0/0

if 'output_path' not in os.listdir():
    os.system("mkdir "+output_path)

os.system("xcopy -r "+input_path+ " "+output_path)

files_list = os.listdir(input_path)
for i in files_list:
    if i.split('.')[-1] != 'jpg' : 
        continue
    image_path = input_path+'\\' + i
    bbox_path  = image_path.replace('.jpg', '.txt')
    _filename = image_path.split('\\')[-1].split('.')[0]
    
    # 이미지와 바운딩 박스 정보 불러오기
    image = imageio.imread(image_path)
    with open(bbox_path, 'r') as f:
        bbox_data = f.readlines()
    
    # 바운딩 박스 정보를 imgaug 형식으로 변환
    bbs = []
    height, width, _ = image.shape
    
    for bbox in bbox_data:
        bbox = bbox.strip().split()
        x, y, w, h = float(bbox[1]), float(bbox[2]), float(bbox[3]), float(bbox[4])
        bbs.append(BoundingBox(x1=(x-(w/2))*width, y1=(y-(h/2))*height, x2=(x+(w/2))*width, y2=(y+(h/2))*height))
        #print(bbs)
    bbs = BoundingBoxesOnImage(bbs, shape=image.shape)
    
    # Augmentor 설정
    seq_list = [
        iaa.Sequential([
            iaa.Fliplr(p=1),   # 좌우반전
        ]),
        iaa.Sequential([
            iaa.Flipud(p=1),   # 상하반전
        ]),
        iaa.Sequential([
            iaa.GaussianBlur(sigma=(0.1, 0.4)), # 블러
            iaa.Affine(
                scale={"x": (0.5, 0.9), "y": (0.5, 0.9)} #가로 세로 비율 망치
            ),
            iaa.BlendAlphaSomeColors(iaa.Grayscale(1.0)) # 색 변조 + 가리기?
        ]),
        iaa.Sequential([
            iaa.PerspectiveTransform(scale=(0.01, 0.2)), # 원근감 왜곡
        ]),
        iaa.Sequential([
            iaa.Affine(
                translate_percent={"x": (-0.5, 0.5), "y": (-0.5, 0.5)} #x,y방향으로 퍼센테이지 이
            )
        ]),
        iaa.Sequential([
            iaa.Fliplr(p=1),   # 좌우반전
            iaa.PerspectiveTransform(scale=(0.01, 0.2)), # 원근감 왜곡
            iaa.Affine(
                shear=(-16, 0) # 기울이기
            ),
        ]),
        iaa.Sequential([
            iaa.Affine(
                rotate=(0, 120), # 회전
                shear=(0, 16) # 기울이기
            ),
            iaa.GaussianBlur(sigma=(0.1, 0.5)), # 블러
            
        ])
    ]

    # 원본 저장
    imageio.imwrite(output_path + '/' +  f'{_filename}_original.jpg', image)
    origin_label = open(output_path+f'/{_filename}_original.txt', 'w')
    for bbox in bbox_data:
        origin_label.write(bbox)
    origin_label.close()
    
    for i in range(REPEAT):
        seq = random.choice(seq_list)
        #seq_list.remove(seq)
        # Augmentation 수행  
        augmented = seq(image=image, bounding_boxes=bbs)
        aug_image = augmented[0]
        aug_bbs = augmented[1]

        # 증강된 이미지 저장
        imageio.imwrite(output_path + '/' +  f'{_filename}_aug{i}.jpg', aug_image)
    
        def clamp(num) :
            if num < 0.0:
                return 0
            if num > 1.0:
                return 1
            return num
    
        # 증강된 바운딩 박스 정보 출력
        with open(output_path + '/' + f'{_filename}_aug{i}.txt', 'w') as f:
            for bbox in aug_bbs.bounding_boxes:
                x1, y1, x2, y2 = bbox.x1, bbox.y1, bbox.x2, bbox.y2
                x = clamp(( ((bbox.x2 + bbox.x1)/2) /aug_bbs.shape[1]))
                y = clamp(( ((bbox.y2 + bbox.y1)/2) /aug_bbs.shape[0]))
                w = clamp(((bbox.x2 - bbox.x1)/aug_bbs.shape[1]))
                h = clamp(((bbox.y2 - bbox.y1)/aug_bbs.shape[0]))
                f.write(f'0 {x} {y} {w} {h}\n')
