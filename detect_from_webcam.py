import cv2
import torch
import os
import datetime
import winsound
import threading
#####################
# 웹캠 인식 못할 때 변경하는 부분 (기본값 0)
SOURCE = 0
# 경보음 울릴지 말지 설정
ALERT_ON = True
# 객체 검출이 완료된 동영상 파일이 저장될 폴더
OUTPUT_FOLDER = "detected"
# (객체 검출과 상관 없이) 동영상 파일이 저장될 폴더. 임시파일 저장용으로도 사용됨
OUTPUT_FOLDER_TEMP = "cctv"
# CCTV 영상 저장할지 말지 여부
CCTV_SAVE = False
# 최소 확률
MINIMUM_POSSIBILITY= 0.6
# 최소 시간(초) : 10초 중에서 최소 몇초 이상은 검출되어야 한다.
MINIMUM_SEC = 1.0
# 모델 객체검출 작동 간격(초) : 해당 간격마다 YOLOv5 객체검출을 시행한다.
MODEL_DETECT_GAP = 0.33333333333333333
# 모델 파일 이름
MODEL_PATH = "shoppingcart_model.pt"
# FPS
FPS = 20.0
# 웹캠 해상도
RESOLUTION = (480, 270)
# 관측창 해상도 바꿀지 여부 (안바꾸면 위에서 설정한 웹캠 해상도 그대로 보임) 
VIEW_RESIZE = False
# 관측창 해상도
VIEW_RESOLUTION = (960, 640)
# 경고음 파일 경로
ALERT_SOUND = "alert.wav"
#####################
def retNowMP4String():
    return "%04d%02d%02d_%02d%02d%02d.mp4" % (datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day, datetime.datetime.today().hour, datetime.datetime.today().minute, datetime.datetime.today().second)

def retNowTime() :
    return "%04d.%02d.%02d %02d:%02d:%02d" % (datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day, datetime.datetime.today().hour, datetime.datetime.today().minute, datetime.datetime.today().second)
# 비동기처리용 전역변수...
is_sound_playing = False
class SoundWorker(threading.Thread):
    def __init__(self):
        super().__init__()
    def run(self):
        global is_sound_playing
        if not ALERT_ON:
            return
        if not is_sound_playing:
            is_sound_playing = True
            winsound.PlaySound(ALERT_SOUND, winsound.SND_FILENAME)
            is_sound_playing = False
        else:
            return

def forResize1(frame) :
    return cv2.resize(frame, dsize=VIEW_RESOLUTION)
def forResize0(frame) :
    return frame
#####################
model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH)
if OUTPUT_FOLDER_TEMP not in os.listdir():
    os.system("mkdir " + OUTPUT_FOLDER_TEMP)
if OUTPUT_FOLDER not in os.listdir():
    os.system("mkdir " + OUTPUT_FOLDER)

# 웹캠 비디오 캡처 객체 생성
cap = cv2.VideoCapture(SOURCE)
# 비디오 코덱 설정
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
now_frame = 0
detect_frames = 0
minimum_sec_to_frames = int(MINIMUM_SEC * FPS)
model_detect_gap_frame = int(MODEL_DETECT_GAP * FPS)
out = None #초기화용
is_detected = False
start_point = None #초기화
end_point = None #초기화
results_refine = None #초기화
possibility = 0.0 #초기화
now_file_name = "" # 초기화
if VIEW_RESIZE:
    resizeFunc = forResize1
else:
    resizeFunc = forResize0

while True:
    if now_frame % int(10*FPS) == 0:
        if now_frame != 0:
            out.release()
            if detect_frames >= minimum_sec_to_frames:
                os.system("copy " +OUTPUT_FOLDER_TEMP+'\\'+now_file_name+ " " +OUTPUT_FOLDER+'\\'+now_file_name)
            if not CCTV_SAVE:
                os.system("del " +OUTPUT_FOLDER_TEMP+'\\'+now_file_name)
        now_file_name = retNowMP4String()
        out = cv2.VideoWriter(OUTPUT_FOLDER_TEMP+'/'+now_file_name, fourcc, FPS, RESOLUTION)
        detect_frames = 0
    # 웹캠에서 프레임 읽기
    ret, frame = cap.read()
    # 프레임이 제대로 읽혔는지 확인
    if not ret: break
    # 사이즈 재조정
    frame = cv2.resize(frame, dsize=(RESOLUTION))
    if now_frame % model_detect_gap_frame == 0:
        predicts = model(frame)
        results_refine = predicts.pandas().xyxy[0].values
        detected_shopping_carts = len(results_refine)
        is_detected = False
        if detected_shopping_carts > 0:
            for bbox in results_refine:
                if(bbox[-3] < MINIMUM_POSSIBILITY) :
                    continue
                is_detected = True
    if is_detected:
        SoundWorker().start()
        detect_frames += 1
        for bbox in results_refine:
            start_point = (int(bbox[0]), int(bbox[1]))
            end_point = (int(bbox[2]), int(bbox[3]))    
            frame = cv2.rectangle(frame, start_point, end_point, (255, 0, 0), 3)
            frame = cv2.putText(frame, '%.1f%%'%(bbox[-3]*100), start_point, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
    frame = cv2.putText(frame, retNowTime(), (0,23), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    # 녹화된 프레임을 비디오 파일에 저장
    out.write(frame)
    # 프레임 출력
    cv2.imshow('Webcam', resizeFunc(frame))
    now_frame += 1
    # 'q' 키를 누르면 녹화 종료
    keyinput = cv2.waitKey(1)
    if keyinput == ord('q') or keyinput == 27: #27은 ESC키의 키코드값
        break

# 사용한 객체 해제
cap.release()
out.release()
os.system("del " +OUTPUT_FOLDER_TEMP+'\\'+now_file_name)
cv2.destroyAllWindows()
