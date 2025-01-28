# import cv2
# import numpy as np
# from PyQt5.QtCore import pyqtSignal, Qt, QThread
#
# #Khai báo class điểm danh khuôn mặt
# class attendance_face(QThread):
#     signal3 = pyqtSignal(np.ndarray)
#     def __init__(self, index):
#         super(attendance_face, self).__init__()
#         self.device = None
#         # self.out_file = None
#         self.classes = None
#         # self.model = None
#         self.gg = True
#         self.player = None
#         self.index = index
#     # Hàm chạy luồng
#     def run(self):
#         self.gg = True
#         self.run_program()  # Hàm chạy chương trình chính
#
#     # Hàm dừng chương trình
#     def stop(self):
#         # print("stop threading", self.index)  # Ghi ra màn hình dừng phát luồng
#         cv2.destroyAllWindows()  # Huỷ cửa sổ Camera
#         self.terminate()  # Hàm dừng luồng
#     # Hàm cho điều kiện While True sai
#     def pause_stream(self):
#         self.gg = False
#
#     #Hàm chạy chương trình chính
#     def run_program(self):
#         #Đọc dữ liệu từ file
#         f = open("link_camera/link_cam_set.txt", mode = "r", encoding="utf-8-sig")
#         link_cam = f.readline().strip()
#         if link_cam == "0" or link_cam == "1" or link_cam == "2":
#             link_cam = int(link_cam)
#         else:
#             link_cam = link_cam
#         #Thêm camera
#         cam = cv2.VideoCapture(link_cam)
#         f.close()
#         #Lấy ID
#         f = open("link_camera/id.txt", mode = "r", encoding="utf-8-sig")
#         face_id = f.readline().strip()
#         f.close()
#
#         #Khai báo thư viện phát hiện khuôn mặt
#         face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#
#         # #Tạo ID khuôn mặt
#         # face_id = input('Mời nhập ID khuôn mặt:')
#         # face_name = input("Mời nhập tên:")
#
#         #Biến đếm số ảnh
#         count = 0
#         #Vòng lặp chính
#         while True:
#             ret, img = cam.read()   #Đọc ảnh từ cam
#             img = cv2.flip(img,1)  #Xoay ảnh lật lên trên
#             gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Chuyển ảnh sang màu thang xám
#             faces = face_detector.detectMultiScale(gray, 1.3,5) #Nhận diện khuôn mặt
#             print(faces, count)
#             for (x, y, w, h) in faces:
#                 cv2.rectangle(img,(x,y),(x + w,y + h), (255,0,0), 2) #Vẽ hình vuông lên khuôn mặt
#                 count += 1
#
#                 cv2.imwrite(f"dataset/User.{face_id}.{count}.jpg", gray[y:y + h, x: x + w])
#                 a = cv2.resize(img, (360,500))
#                 # cv2.imshow("Anh", img)
#             # if cv2.waitKey(1) == ord("q"):
#             #     break
#             if count >= 50:
#                 break
#             else:
#                 pass
#             #TRUYỀN TÍNH HIỆU VỀ
#             self.signal3.emit(img)
#             if not self.gg:
#                 break
