#-*- coding:utf-8 -*-
import torch
import cv2
import os
import tkinter as tk
from tkinter import filedialog
##############
# 동영상 파일 이름
VIDEO = "초기화용이름.mp4"
# 객체 검출이 완료된 동영상 파일이 저장될 폴더
OUTPUT_FOLDER = "detected_videos"
# 최소 확률
MINIMUM_POSSIBILITY= 0.6
# 최소 시간(초) : 10초 중에서 최소 몇초 이상은 검출되어야 한다.
MINIMUM_SEC = 1.0
# 모델 객체검출 작동 간격(초) : 해당 간격마다 YOLOv5 객체검출을 시행한다.
MODEL_DETECT_GAP = 0.33333333333333333
# 모델 파일 이름
MODEL_PATH = "shoppingcart_model.pt"
# 동영상 파일을 임시로 처리할 폴더
OUTPUT_FOLDER_TEMP = "_tmp"
##############
def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])
    entry_video.delete(0, tk.END)
    entry_video.insert(0, filename)
    
def save_settings():
    global can_I_run
    global VIDEO
    global OUTPUT_FOLDER
    global MINIMUM_POSSIBILITY
    global MINIMUM_SEC
    global MODEL_DETECT_GAP
    global MODEL_PATH
    global OUTPUT_FOLDER_TEMP
    VIDEO = entry_video.get()
    OUTPUT_FOLDER = entry_output_folder.get()
    MINIMUM_POSSIBILITY = float(entry_min_possibility.get())
    MINIMUM_SEC = float(entry_min_sec.get())
    MODEL_DETECT_GAP = float(entry_model_detect_gap.get())
    MODEL_PATH = entry_model_path.get()
    OUTPUT_FOLDER_TEMP = entry_output_folder_temp.get()
    can_I_run = True
    # 창 닫기
    root.destroy()
root = tk.Tk()

can_I_run = False

# 동영상 파일 이름 입력 창
label_video = tk.Label(root, text="동영상 파일 이름:")
label_video.pack()

entry_video = tk.Entry(root, width=50)
entry_video.pack()

button_browse = tk.Button(root, text="Browse", command=browse_file)
button_browse.pack()

# 객체 검출이 완료된 동영상 파일이 저장될 폴더 입력 창
label_output_folder = tk.Label(root, text="객체 검출이 완료된 동영상 파일이 저장될 폴더:")
label_output_folder.pack()

entry_output_folder = tk.Entry(root, width=50)
entry_output_folder.pack()
entry_output_folder.insert(0, OUTPUT_FOLDER)

# 최소 확률 입력 창
label_min_possibility = tk.Label(root, text="최소 확률:")
label_min_possibility.pack()


entry_min_possibility = tk.Entry(root, width=50)
entry_min_possibility.pack()
entry_min_possibility.insert(0, str(MINIMUM_POSSIBILITY))

# 최소 시간(초) 입력 창
label_min_sec = tk.Label(root, text="최소 시간(초):")
label_min_sec.pack()

entry_min_sec = tk.Entry(root, width=50)
entry_min_sec.pack()
entry_min_sec.insert(0, str(MINIMUM_SEC))

# 모델 객체검출 작동 간격(초) 입력 창
label_model_detect_gap = tk.Label(root, text="모델 객체검출 작동 간격(초):")
label_model_detect_gap.pack()

entry_model_detect_gap = tk.Entry(root, width=50)
entry_model_detect_gap.pack()
entry_model_detect_gap.insert(0, str(MODEL_DETECT_GAP))

# 모델 파일 이름 입력 창
label_model_path = tk.Label(root, text="모델 파일 이름:")
label_model_path.pack()

entry_model_path = tk.Entry(root, width=50)
entry_model_path.pack()
entry_model_path.insert(0, MODEL_PATH)

# 동영상 파일을 임시로 처리할 폴더 입력 창
label_output_folder_temp = tk.Label(root, text="동영상 파일을 임시로 처리할 폴더:")
label_output_folder_temp.pack()

entry_output_folder_temp = tk.Entry(root, width=50)
entry_output_folder_temp.pack()
entry_output_folder_temp.insert(0, OUTPUT_FOLDER_TEMP)

# 저장 버튼
button_save = tk.Button(root, text="Save", command=save_settings)
button_save.pack()

root.mainloop()
#

if(not can_I_run):
    os._exit(0)
    
model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH)
def classifyVideo(videoFileName, tmp_output_folder):
    cap = cv2.VideoCapture(tmp_output_folder+'/'+videoFileName)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    model_detect_gap_frame = int(MODEL_DETECT_GAP * fps)
    current_frame = 0
    detect_frames = 0
    minimum_sec_to_frames = int(MINIMUM_SEC * fps)
    is_detected = False
    start_point = None #초기화
    end_point = None #초기화
    results_refine = None #초기화
    possibility = 0.0 #초기화
    ret, frame = cap.read()
    new_file_name = tmp_output_folder+'\\'+videoFileName.split('.mp4')[0]+"_detected"+".mp4"
    output = cv2.VideoWriter(new_file_name, cv2.VideoWriter_fourcc(*"mp4v"), fps, (frame.shape[1], frame.shape[0]))
    while True:
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
        ret, frame = cap.read()
        if not ret:
            break
        if current_frame % model_detect_gap_frame == 0:
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
            detect_frames += 1
            for bbox in results_refine:
                start_point = (int(bbox[0]), int(bbox[1]))
                end_point = (int(bbox[2]), int(bbox[3]))    
                frame = cv2.rectangle(frame, start_point, end_point, (255, 0, 0), 3)
                frame = cv2.putText(frame, '%.1f%%'%(bbox[-3]*100), start_point, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
        output.write(frame)
        current_frame += 1
    output.release()
    cap.release()
    if detect_frames < minimum_sec_to_frames:
        os.system("del "+new_file_name)
    os.system("del " + tmp_output_folder+"\\"+videoFileName)
    return
#############################
current_path = os.path.abspath(__file__)
directory_path = os.path.dirname(current_path)
os.chdir(directory_path)

if OUTPUT_FOLDER_TEMP not in os.listdir():
    os.system("mkdir " + OUTPUT_FOLDER_TEMP)
if OUTPUT_FOLDER not in os.listdir():
    os.system("mkdir " + OUTPUT_FOLDER)
print(".\\ffmpeg.exe -i \""+VIDEO+"\" -c copy -map 0 -segment_time 00:00:10 -f segment \""+OUTPUT_FOLDER_TEMP+"\\output_%8d0.mp4\"")

os.system(".\\ffmpeg.exe -i \""+VIDEO+"\" -c copy -map 0 -segment_time 00:00:10 -f segment \""+OUTPUT_FOLDER_TEMP+"\\output_%8d0.mp4\"")

files_list = os.listdir(OUTPUT_FOLDER_TEMP)
for i in range(0, len(files_list)):
    print("Progressing... (%d/%d)" % (i+1, len(files_list)))
    if files_list[i].split('.')[-1] == 'mp4':
        classifyVideo(files_list[i], OUTPUT_FOLDER_TEMP)

os.system("for %F in ("+OUTPUT_FOLDER_TEMP+"\\*.mp4) do move \"%F\" "+OUTPUT_FOLDER+"\\")
