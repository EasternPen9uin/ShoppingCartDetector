HEIGHT = 600
###############
import os
import tkinter as tk
from PIL import ImageTk, Image

################
def moveToPositive(filename) :
    os.system("move PHOTOS\\"+filename+" POSITIVE")
def moveToNegative(filename) :
    os.system("move PHOTOS\\"+filename+" NEGATIVE")
def moveToAmbi(filename) :
    os.system("move PHOTOS\\"+filename+" AMBIGUOUS")
def nextImage() :
    global current_image_index
    global image
    global photo
    global label
    current_image_index += 1  # 다음 이미지 인덱스 계산
    image = Image.open("PHOTOS\\"+image_paths[current_image_index])  # 이미지 로드
    image = image.resize((int((HEIGHT * image.size[0])/image.size[1]), HEIGHT), Image.ANTIALIAS)  # 이미지 크기 조정
    photo = ImageTk.PhotoImage(image)  # 이미지를 PhotoImage 객체로 변환
    label.configure(image=photo)  # 라벨에 이미지 배치
    print("파일이름:",image_paths[current_image_index])
def buttonFuncPositive():    
    moveToPositive(image_paths[current_image_index])
    nextImage()
def buttonFuncNegative():
    moveToNegative(image_paths[current_image_index])
    nextImage()
def buttonFuncAmbi():
    moveToAmbi(image_paths[current_image_index])
    nextImage()

################
if "PHOTOS" not in os.listdir():
    input("PHOTOS 폴더가 없습니다!")
    os._exit(-1)

if "POSITIVE" not in os.listdir():
    os.system("mkdir POSITIVE")
if "NEGATIVE" not in os.listdir():
    os.system("mkdir NEGATIVE")
if "AMBIGUOUS" not in os.listdir():
    os.system("mkdir AMBIGUOUS")
image_paths = os.listdir("PHOTOS")

current_image_index = 0

# tkinter 윈도우 생성
root = tk.Tk()

# 이미지 로드 및 크기 조정
image = Image.open("PHOTOS\\"+image_paths[current_image_index])
image = image.resize((int((800 * image.size[0])/image.size[1]), HEIGHT), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)

# 라벨에 이미지 배치
label = tk.Label(image=photo)
label.pack()

# 버튼 놓을 프레임 생성
frame = tk.Frame(root)
frame.pack(side="top", padx=10, pady=10)

# 버튼 생성
button1 = tk.Button(frame, text="POSITIVE", command=buttonFuncPositive, width=20, height=10)
button2 = tk.Button(frame, text="NEGATIVE", command=buttonFuncNegative, width=20, height=10)
button3 = tk.Button(frame, text="AMBIGUOUS", command=buttonFuncAmbi, width=20, height=10)


# 버튼 배치
button1.pack(side="left", padx=5)
button2.pack(side="left", padx=5)
button3.pack(side="left", padx=5)

# 창 실행
root.mainloop()
