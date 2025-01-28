from PyQt5.QtCore import QThread, pyqtSignal,Qt
import playsound
import keras
import cv2
import numpy as np
import mediapipe as mp
from def_important import mediapipe_detection, draw_style_landmarks, extract_keypoints, send_photos_far_quay_cop, send_photos_far_sleep, send_photos_giam_sat_rong, send_photos_giam_sat_ngu
import tkinter as tk
from tkinter import messagebox
from tkinter import *
import os
import tkinter as tk
from tkinter import messagebox
import time
import torch
class detect_far(QThread):
    signal6 = pyqtSignal(np.ndarray)
    def __init__(self, index):
        super(detect_far, self).__init__()
        self.device = None
        # self.out_file = None
        self.classes = None
        # self.model = None
        self.gg = True
        self.player = None
        self.index = index
    # Hàm chạy luồng
    def run(self):
        self.gg = True
        self.run_program()  # Hàm chạy chương trình chính

    # Hàm dừng chương trình
    def stop(self):
        self.gg = False
        self.wait()
        cv2.destroyAllWindows()
        self.terminate()  # Hàm dừng luồng

    # Hàm cho điều kiện While True sai
    def pause_stream(self):
       pass

    #Hàm chạy chương trình chính
    def run_program(self):

        print("Nhận luồng")
        mp_holistic = mp.solutions.holistic #Khởi tạo hàm nhận dạng
        #Load model
        model = keras.models.load_model('hanhdong.h5') # ví dụ: đọc mô hình từ tệp h5
        model1 = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        # Khởi tạo cấu trúc vẽ
        mp_drawing = mp.solutions.drawing_utils
        sequence = []   #Mảng chứa tên hành động
        sentence = []   #Mảng chứa độ chính xác
        actions = np.array(["Dang kiem tra", "Quay cop","Ngu"])
        threshold = 0.5 #Độ chính xác cần nhận dạng
        predictions = []
        colors = [(245,117,16), (117,245,16), (16,117,245)] #Bảng màu sắc

        #Hàm vẽ các hành động trên cam
        def prob_viz(res, actions, input_frame, colors):
            output_frame = input_frame.copy()
            for num, prob in enumerate(res):
                cv2.rectangle(output_frame, (0,60+num*40), (int(prob*100), 90+num*40), colors[num], -1)
                cv2.putText(output_frame, actions[num], (0, 85+num*40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            return output_frame
        #Đọc dữ liệu cho camera
        f = open("Link_camera/link_data_camera.txt",mode = "r",encoding="utf-8-sig")
        a = f.readline().strip()
        if str(a) == "0" or str(a) == "1" or str(a) == "2" or str(a) == "3" or str(a) == "4":
            link_cam = int(a)   #Set khi camera nhập từ phím
        else:
            link_cam = str(a)
        print(link_cam)
        cap = cv2.VideoCapture(link_cam)    #Lấy camera
        # Mảng điều kiện
        fraud = 0  # Mảng chứa số lần quay cóp
        sleep = 0  # Mảng chứa số lần ngủ
        kiem_tra_quay_cop = 0
        kiem_tra_ngu = 0
        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            while True:
                # Đọc camera
                ret, frame = cap.read()

                # Lấy toạ độ các điểm
                image, results = mediapipe_detection(frame, holistic)
                # print(results)
                # Vẽ các điểm lên cơ thể
                draw_style_landmarks(image, results)

                # Logic tính toán
                keypoints = extract_keypoints(results)
                sequence.append(keypoints)
                sequence = sequence[-30:]
                # Điều kiện thoả mãn nhận dạng
                if len(sequence) == 30:
                    res = model.predict(np.expand_dims(sequence, axis=0))[0]
                    # print(actions[np.argmax(res)])
                    predictions.append(np.argmax(res))

                    if np.unique(predictions[-10:])[0] == np.argmax(res):
                        if res[np.argmax(res)] > threshold:
                            if len(sentence) > 0:
                                if actions[np.argmax(res)] != sentence[-1]:
                                    sentence.append(actions[np.argmax(res)])
                            else:
                                sentence.append(actions[np.argmax(res)])

                    if len(sentence) > 5:
                        sentence = sentence[-5:]

                    # # Viz probabilities
                    image = prob_viz(res, actions, image, colors)

                # Hiển thị camera
                anh = cv2.resize(image, (450, 250))
                # cv2.imshow('OpenCV Feed', anh)
                # Trả dữ liệu về luồng
                print("Bắt đầu trả về dữ liệu")
                self.signal6.emit(anh)
                print("Kết thúc trả về dữ liệu")
                # Hàm kiểm tra
                if len(sentence) != 0:
                    print("Hành động là:", sentence[0])
                    # Điều kiện chính
                    if str(sentence[0]) == "Dang kiem tra":
                        pass
                    elif str(sentence[0]) == "Ngu":
                        sleep += 1

                    elif str(sentence[0]) == "Quay cop":
                        fraud += 1

                #Điều kiện phát hiện gian lận

                #Điều kiện nhắc nhở:
                if sleep > 30:
                    print("Dừng ngủ")
                    playsound.playsound("Audio/sleep.mp3")
                    cv2.waitKey(5000)
                    sleep = 0
                    kiem_tra_ngu += 1
                    cv2.imwrite("Image/hoc_sinh_ngu.png", frame)
                    send_photos_giam_sat_rong()
                if fraud > 30:
                    print("Dừng quay cóp")
                    playsound.playsound("Audio/nghiemtuc.mp3")
                    kiem_tra_quay_cop += 1
                    fraud = 0
                    cv2.imwrite("Image/hoc_sinh_ngu.png", frame)
                    send_photos_giam_sat_rong()
                    #Điều kiện phát hiện quay cóp
                if kiem_tra_quay_cop >=3:
                    playsound.playsound("Audio/fraud.mp3")
                    # cv2.imwrite("Image/hoc_sinh_quay_cop.png",frame)
                    cv2.imwrite("Image/hoc_sinh_ngu.png",frame)
                    send_photos_giam_sat_rong()
                    break

                if kiem_tra_ngu >=8:
                    playsound.playsound("Audio/thong_bao.mp3")
                    cv2.imwrite("Image/hoc_sinh_rong.png",frame)
                    send_photos_giam_sat_ngu()
                    break
                if self.gg == False:
                    break

        cap.release()
        cv2.destroyAllWindows()
        self.quit()
        self.wait()
