# ShoppingCartDetector

아래 사이트를 참고해주십시오. 
노션 주소 : https://swamp-country-c8e.notion.site/OpenCV-5bff4577d0574c8d8474035c11202824

2023학년도 1학기 한양대학교 AI-X:딥러닝 과목 팀 프로젝트인 "OpenCV, YOLOv5를 이용한 쇼핑카트 도난 방지 시스템"의 
소스코드 및 결과물로서의 프로그램의 압축파일입니다.
코드는 파이썬으로 작성되었으며 일부 프로그램 내에서 ffmpeg 6.0-essentials_build (https://github.com/GyanD/codexffmpeg)
를 사용합니다. 또한 pytorch와 opencv라이브러리를 사용합니다.
여담으로 이 프로그램은 윈도우 OS에서만 정상동작하며, 파이썬 임베드를 사용하였으므로 파이썬 설치나 라이브러리 설치 없이 
바로 실행 가능합니다.

소스코드가 아닌, 프로그램 실행파일 및 데이터셋은 아래 주소에서 다운받아주십시오 :
https://drive.google.com/drive/folders/1jGkT2vGaieE7pOCnmoDCGUxnirFFtjdN?usp=share_link

아래는 실행파일 관련 설명입니다.

* /Win64_CPU.zip : 
  CPU 버전으로 작동하는 프로그램의 압축파일입니다. 실행하려면 "쇼핑카트_비디오_판독기.cmd" 파일 또는  
  "쇼핑카트_경보기_및_CCTV.cmd" 파일을 실행하면 됩니다. 
  CPU기반으로 작동하므로 Nvidia 그래픽카드가 없어도 동작은 하나, 컴퓨터 환경에 따라 느리게 동작할 수 있습니다.
* /Win64_GPU.zip :
  GPU 버전으로 작동하는 프로그램의 압축파일입니다. Win64_CPU.zip와 거의 동일하나 cuda10.2버전을 사용하므로 
  Nvidia 그래픽카드가 있어야 동작하나, 대신 빠르게 동작합니다. 그래픽카드 종류에 따라 cuda10.2버전을 지원하지 
  않는다면 동작하지 않을 수 있습니다. 
  
각 프로그램의 역할은 다음과 같습니다 : 
* "쇼핑카트_비디오_판독기.cmd" :
  동영상 파일에서 쇼핑카트가 등장하는 부분만 10초 단위로 분할하여 저장하는 프로그램입니다.
* "쇼핑카트_경보기_및_CCTV.cmd" : 
  웹캠을 사용해 영상을 10초 단위로 녹화시키면서 쇼핑카트가 감지되었을 경우 경보음을 
  재생시키는 프로그램입니다. 쇼핑카트가 나온 구간만 녹화시킬지 말지 설정 가능하며, 기본값은 
  쇼핑카트 영역만 저장하도록 되어있습니다. (설정 변경하려면 detect_from_webcam.py 파일 내 
  설정을 바꾸면 됩니다.)


아래는 소스코드 관련 설명입니다:

* /models : 
  Pytorch로 학습된 쇼핑카트 이미지 검출 모델 파일 및 테스트 결과를 모아놓은 폴더입니다.
  각 모델 파일은 Model(숫자)_(사용된 optimizer 설정).pt 형식의 이름으로 되어있으며,
  Model1_SGD와 Model2_Adam_ruined의 경우 lr0을 0.01로, Model3_Adam과 Model4_AdamW의 경우 
  lr0을 0.001로 설정하여 각 모델별로 epoch 100씩 학습시켰습니다. 
  results_Model(숫자)_(사용된 optimizer 설정).csv의 형식으로 된 파일은 각 모델별 epoch별로
  YOLOv5의 train.py가 자동 생성한 결과 파일이며, 
  best_validation.csv, best_test.csv파일은 각 모델의 최종결과물(best.pt) 4개를 val.py를
  사용하여 validation set과 test set에 각각 평가하여 나온 결과를 기록한 파일입니다.
  
* /used_to_make_datasets : 
  데이터셋을 만들 때 사용한 파이썬 코드를 모아놓은 폴더입니다. 
  1_img_to_jpg.py : 
    폴더 안에 있는 이미지 파일을 모두 jpg파일로 바꾸는 코드입니다.
	실행하려면 PIL 라이브러리가 필요합니다.
  2_IMAGE_CLASSIFIER_BY_HUMAN.py : 
    이미지 파일의 분류를 용이하게 하기 위한 코드입니다. 
  3_making_zero_label.py : 
    검출할 물체가 없는 이미지의 YOLO라벨을 만들기 위한 코드입니다.
  4_img_aug.py : 
    이미지를 imgaug 라이브러리를 활용하여 증강시키는 코드입니다.
	실행하려면 imgaug 라이브러리의 설치가 필요합니다.
	
* /alert.wav :
  파이썬 gtts 라이브러리로 생성한 경고음 사운드입니다.
  
* /detect_from_video.py : 
  동영상 파일에서 쇼핑카트가 등장하는 부분만 10초 단위로 분할하여 저장하는 프로그램입니다.
  실행하려면 opencv라이브러리와 pytorch 라이브러리, 그리고 ultralytics라이브러리가 필요하며,
  코드와 같은 폴더 내에 ffmpeg.exe 파일, 그리고 쇼핑카트 모델 파일이 필요합니다. 
  
* /detect_from_video.py : 
  웹캠을 사용해 영상을 10초 단위로 녹화시키면서 쇼핑카트가 감지되었을 경우 경보음을 
  재생시키는 프로그램입니다. 쇼핑카트가 나온 구간만 녹화시킬지 말지 설정 가능하며, 기본값은 
  쇼핑카트 영역만 저장하도록 되어있습니다.
  실행하려면 opencv라이브러리와 pytorch 라이브러리, 그리고 ultralytics라이브러리가 필요하며,
  코드와 같은 폴더 내에 쇼핑카트 모델 파일과 경고음 파일이 필요합니다.
  
* /shoppingcart_model.pt : 
  YOLOv5 쇼핑카트 모델입니다. /models/Model1_SGD.pt 파일과 동일한 파일입니다.
  
아래는 데이터셋 관련 설명입니다. 
* /custom_dataset.7z :
  모델 학습시에 사용된 데이터셋입니다.
  쇼핑카트 이미지는 canva, unsplash, pexels, pixabay에서 퍼블릭 도메인 쇼핑카트 이미지를 구한 후 증강시켰고,
  쇼핑카트가 아닌 이미지는 
    Bicycle Image Dataset
	  (https://www.kaggle.com/datasets/dataclusterlabs/bicycle-image-dataset-vehicle-dataset?resource=download)
	COCO 2014 Dataset (for YOLOv3) 
	  (https://www.kaggle.com/datasets/jeffaudi/coco-2014-dataset-for-yolov3)
  에서 일부를 사용하였습니다.
