import datetime

import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QMutex, QWaitCondition
from imutils.video import VideoStream
import cv2
from DEF_NEW import *
import mediapipe as mp
from playsound import *
import telegram

import asyncio

#Tạo lớp gọi 2 cam
class Camera_new(QThread):
    signal1_far = pyqtSignal(np.ndarray)
    signal2_far = pyqtSignal(np.ndarray)
    signal_main_far = pyqtSignal(np.ndarray)
    def __init__(self, index):
        super(Camera_new, self).__init__()
        self.gg = True
        self.index = index
    # Hàm chạy luồng
    def run(self):
        self.gg = True
        self.run_program()  # Hàm chạy chương trình chính
    # Hàm dừng chương trình
    def stop(self):
        self.gg = False
        # self.wait()
        # cv2.destroyAllWindows()  # Huỷ cửa sổ Camera
        # self.terminate()
    # Hàm cho điều kiện While True sai
    def pause_stream(self):
        pass

    def send_photos_vp_to_telegram(self, option, cap):
        files = open("Telegram_bot/token.txt", "r")
        mang = []
        a = files.read()
        mang = a.split(",")
        mang_xuli = []
        for i in range(2):
            dt = str(mang[i])
            dt.replace(" ", "")
            mang_xuli.append(dt)
        my_token = mang[0]  # ID
        id = mang[1]  # Token
        # Gọi bot
        bot = telegram.Bot(token=my_token)
        link_anh = r'Image_student/hoc_sinh_' + str(option) + '.png'
        image = open(link_anh, "rb")
        asyncio.run(bot.sendPhoto(chat_id=id, photo=open(link_anh, "rb"), caption=cap))
    #Hàm chạy chương trình chính
    def run_program(self):
        # print("Khởi động Camera new")
        cam = VideoStream(src=self.index).start()
        # print("Qua bước lấy camera")
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)
        mp_drawing = mp.solutions.drawing_utils
        drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(224, 224, 224))
        #Màu cơ bản
        #Màu vàng
        yellow = (255,255,0)
        pink = (255,0,255)
        red = (255,0,0)
        green = (0,255,0)
        i = 0
        kiem_tra_loi = 0
        kiem_tra_camera_trai = 0
        kiem_tra_camera_phai = 0
        kiem_tra_che_cam_trai = 0
        kiem_tra_che_cam_phai = 0
        sl_camera_trai = 0
        sl_camera_phai = 0
        hs1_sound = 0
        hs1_sound_boolean = False
        hs2_sound_boolean = False
        hs2_sound = 0
        playsound("Audio/start.mp3")
        link = ""
        cap = ""
        # print("Tới vòng lặp")
        while True:
            #Đọc cam
            frame = cam.read()
            # print("Đã đọc dữ liệu")
            # frame = giam_sat(cam)
            # frame = cv2.flip(frame,1)
            #Chỉnh sửa kích thước ảnh
            frame = cv2.resize(frame,(600,300))

            # Lấy kích thước ảnh
            height, width = frame.shape[:2]
            # Tính toán vị trí chia ảnh thành hai phần
            split_point = width // 2
            # Chia ảnh thành hai phần
            left_image = frame[:, :split_point]
            right_image = frame[:, split_point:]
            image_draw = frame
            #Vẽ 1 đường chia đôi màn hình chính
            cv2.line(image_draw,(300,0),(300,300),yellow,4)
            #Vẽ đường chia đôi trên
            # cv2.line(image_draw,(0,100),(600,100),pink,2)
            # #Vẽ đường chia đôi dưới
            # cv2.line(image_draw,(0,200),(600,200),pink,2)
            #Vẽ đường bên trái 1
            #cv2.line(image_draw,(100,0),(100,300),green,2)
            #Vẽ đường bên trái 2
            #cv2.line(image_draw,(200,0),(200,300),green,2)
            #Vẽ đường bên phải 1
            # cv2.line(image_draw,(400,0),(400,300),red,2)
            # #Vẽ đường bên phải 2
            # cv2.line(image_draw,(500,0),(500,300),red,2)
            # #Gạch chéo trái 1
            # cv2.line(image_draw,(100,200),(0,300),(0,255,100),2)
            # #Gạch chéo trái 2
            # cv2.line(image_draw,(200,200),(300,300),(0,255,100),2)
            # #Gạch chéo phải 1
            # cv2.line(image_draw,(400,200),(300,300),(0,255,100),2)
            # #Gạch chéo phải 2
            # cv2.line(image_draw,(500,200),(600,300),(0,255,100),2)

            #Xử lí ảnh Camera 1
            image_1 = xu_li_anh(left_image,face_mesh,mp_face_mesh,mp_drawing,drawing_spec)
            #Xử lí ảnh Camera 2
            image_2 = xu_li_anh_2(right_image,face_mesh,mp_face_mesh,mp_drawing,drawing_spec)

            #Lấy vị trí khuôn mặt 1
            vt_1 = vi_tri_cam_1(left_image,face_mesh,mp_face_mesh,mp_drawing,drawing_spec)
            # print("Vị trí camera 1 là",vt_1)
            vt_2 = vi_tri_cam_2(right_image,face_mesh,mp_face_mesh,mp_drawing,drawing_spec)

            #Tạo hàm điều kiện
            #Xử lí điều kiện camera 1
            if vt_1 == "Trai" or vt_1 == "Phai":
                sl_camera_phai += 1
                if sl_camera_phai == 30:
                    kiem_tra_camera_phai += 1
                    sl_camera_phai = 0
                    hs1_sound += 1
                    hs1_sound_boolean = True
            #Xử lí điều kiện camera bên trái
            if vt_2 == "Trai" or vt_2 == "Phai":
                sl_camera_trai += 1
                if sl_camera_trai == 30:
                    kiem_tra_camera_trai += 1
                    sl_camera_trai = 0
                    hs2_sound += 1
                    hs2_sound_boolean = True
                #Tới buước xử lí điều kiện

            #Hàm điều kiện
            if kiem_tra_camera_trai <= 2 and kiem_tra_camera_phai <=2:
                self.signal1_far.emit(image_1)
                self.signal2_far.emit(image_2)
            elif kiem_tra_camera_trai > 2 and kiem_tra_camera_phai <= 2:
                self.signal1_far.emit(image_1)
            elif kiem_tra_camera_phai > 2 and kiem_tra_camera_trai <= 2:
                self.signal2_far.emit(image_2)
            else:
                pass


            # #Kiểm tra điều kiện để dừng luồng
            #Phát ra âm thanh
            #Nhắc nhở lần 1
            if hs2_sound == 1 and hs2_sound_boolean == True:
                print('hs 2 lan 1')
                playsound("Audio/hs2_lan1.mp3")
                # Lưu ảnh vi phạm học sinh 2
                cv2.imwrite("Image_student/hoc_sinh_2.png", right_image)
                link = "hoc_sinh_2.png"
                cap = "Thí sinh 2 lần 1"
                self.send_photos_vp_to_telegram(option=2, cap=cap)
                hs2_sound_boolean = False
            #Nhắc nhở lần 2
            elif hs2_sound == 2 and hs2_sound_boolean == True:
                print('hs 2 lan 2')

                playsound("Audio/hs2_lan2.mp3")
                # Lưu ảnh vi phạm học sinh 2
                cv2.imwrite("Image_student/hoc_sinh_2.png", right_image)
                link = "hoc_sinh_2.png"
                cap = "Thí sinh 2 lần 2"
                self.send_photos_vp_to_telegram(option=2, cap=cap)
                hs2_sound_boolean = False
            #Nhắc nhở lần 3
            elif hs2_sound == 3 and hs2_sound_boolean == True:
                print('hs 2 lan 3')
                playsound("Audio/phathien.mp3")
                if hs2_sound_boolean == True:
                    #Lưu ảnh vi phạm học sinh 2
                    cv2.imwrite("Image_student/hoc_sinh_2.png",right_image)
                    link = "hoc_sinh_2.png"
                    cap = "Thí sinh 2 vi phạm"
                    self.send_photos_vp_to_telegram(option=2,cap=cap)
                    hs2_sound_boolean = False
            #Phát ra âm thanh
            #Nhắc nhở lần 1
            if hs1_sound == 1 and hs1_sound_boolean == True:
                print('hs 1 lan 1')

                playsound("Audio/hs1_lan1.mp3")
                cv2.imwrite("Image_student/hoc_sinh_1.png", left_image)
                print("2--")

                link = "hoc_sinh_1.png"
                cap = "Thí sinh 1 lần 1"
                self.send_photos_vp_to_telegram(option=1, cap=cap)
                hs1_sound_boolean = False
            #Nhắc nhở lần 2
            elif hs1_sound == 2 and hs1_sound_boolean == True:
                print('hs 1 lan 2')

                playsound("Audio/hs1_lan2.mp3")
                cv2.imwrite("Image_student/hoc_sinh_1.png", left_image)
                print("2--")

                link = "hoc_sinh_1.png"
                cap = "Thí sinh 1 lần 2"
                self.send_photos_vp_to_telegram(option=1, cap=cap)
                hs1_sound_boolean = False
            #Nhắc nhở lần 3
            elif hs1_sound == 3 and hs1_sound_boolean == True:
                print('hs 1 lan 3')

                playsound("Audio/phathien.mp3")
                if hs1_sound_boolean == True:
                    print("1--")
                    #Lưu ảnh vi phạm học sinh 1
                    cv2.imwrite("Image_student/hoc_sinh_1.png",left_image)
                    print("2--")

                    link = "hoc_sinh_1.png"
                    cap = "Thí sinh 1 vi phạm"
                    self.send_photos_vp_to_telegram(option=1, cap=cap)
                    print("3--")

                    hs1_sound_boolean = False
            self.signal_main_far.emit(frame)
            if self.gg == False:
                break
        cam.stop()







#Hàm mở camera để test
class Open_Camera(QThread):
    signal1_op = pyqtSignal(np.ndarray)
    signal2_op = pyqtSignal(np.ndarray)
    signal_main_op = pyqtSignal(np.ndarray)
    signal_stop = pyqtSignal(object)
    def __init__(self, index):
        super(Open_Camera, self).__init__()
        self.gg = True
        self.index = index
    # Hàm chạy luồng
    def run(self):
        self.gg = True
        self.run_program()  # Hàm chạy chương trình chính
    # Hàm dừng chương trình
    def stop(self):
        self.gg = False
        self.wait()
        # cv2.destroyAllWindows()  # Huỷ cửa sổ Camera
        self.terminate()
    # Hàm cho điều kiện While True sai
    def pause_stream(self):
        pass
    #Hàm chạy chương trình chính
    def run_program(self):
        cam = VideoStream(src=self.index).start()
        #Màu cơ bản
        #Màu vàng
        yellow = (255,255,0)
        # pink = (255,0,255)
        # red = (255,0,0)
        # green = (0,255,0)
        i = 0
        # playsound("Audio/start.mp3")
        while True:
            #Đọc cam
            frame = cam.read()
            #Chỉnh sửa kích thước ảnh
            frame = cv2.resize(frame,(600,300))
            # Lấy kích thước ảnh
            height, width = frame.shape[:2]
            # Tính toán vị trí chia ảnh thành hai phần
            split_point = width // 2
            # Chia ảnh thành hai phần
            left_image = frame[:, :split_point]
            right_image = frame[:, split_point:]

            image_draw = frame
            #Vẽ 1 đường chia đôi màn hình chính
            cv2.line(image_draw,(300,0),(300,300),yellow,4)
            #Vẽ đường chia đôi trên
            # cv2.line(image_draw,(0,100),(600,100),pink,2)
            #Vẽ đường chia đôi dưới
            # cv2.line(image_draw,(0,200),(600,200),pink,2)
            #Vẽ đường bên trái 1
            # cv2.line(image_draw,(100,0),(100,300),green,2)
            # Vẽ đường bên trái 2
            # cv2.line(image_draw,(200,0),(200,300),green,2)
            #Vẽ đường bên phải 1
            # cv2.line(image_draw,(400,0),(400,300),red,2)
            #Vẽ đường bên phải 2
            # cv2.line(image_draw,(500,0),(500,300),red,2)
            #Gạch chéo trái 1
            # cv2.line(image_draw,(100,200),(0,300),(0,255,100),2)
            #Gạch chéo trái 2
            # cv2.line(image_draw,(200,200),(300,300),(0,255,100),2)
            #Gạch chéo phải 1
            # cv2.line(image_draw,(400,200),(300,300),(0,255,100),2)
            #Gạch chéo phải 2
            # cv2.line(image_draw,(500,200),(600,300),(0,255,100),2)
            self.signal_main_op.emit(frame)
            self.signal1_op.emit(left_image)
            self.signal2_op.emit(right_image)
            # cv2.imshow("Camera 1",left_image)
            # cv2.imshow("Camera 2",right_image)
            if self.gg == False:
                break
        cam.stop()







#Hàm mở camera để điểm danh
class Attendace_camera_far(QThread):
    signal1_op_far = pyqtSignal(np.ndarray)
    signal2_op_far = pyqtSignal(np.ndarray)
    signal_main_far = pyqtSignal(np.ndarray)
    signal_data = pyqtSignal(object)

    def __init__(self, index):
        super(Attendace_camera_far, self).__init__()
        self.gg = True
        self.index = index
    # Hàm chạy luồng
    def run(self):
        self.gg = True
        self.run_program()  # Hàm chạy chương trình chính
    # Hàm dừng chương trình
    def stop(self):
        self.gg = False
        self.wait()
        # cv2.destroyAllWindows()  # Huỷ cửa sổ Camera
        self.terminate()
    # Hàm cho điều kiện While True sai
    def pause_stream(self):
        pass
    #Hàm chạy chương trình chính
    # def run_program(self):
    #     kiemtra = True
    #     dectector = cv2.QRCodeDetector()  # Nhận dạng
    #     print("Chạy luồng 4")
    #     recognizer = cv2.face.LBPHFaceRecognizer_create()
    #     recognizer.read('trainer.yml')
    #     cascadePath = 'haarcascade_frontalface_default.xml'
    #     faceCascade = cv2.CascadeClassifier(cascadePath)
    #     font = cv2.FONT_HERSHEY_SIMPLEX
    #     #Khởi tạo biến ID
    #     id = 0
    #     #Đọc file cam
    #     f = open("link_camera/link_cam_detect.txt", mode = "r", encoding="utf-8-sig")
    #     link = f.readline().strip()
    #     f.close()
    #     if link == "0" or link == "1" or link == "2":
    #         link = int(link)
    #     else:
    #         link = link
    #
    #     #Mở file chứa thông tin học sinh ra
    #     f = open("info_student/model.csv", mode= "r",encoding = "utf-8-sig")
    #     #Đọc dòng thứ 1 của file
    #     header = f.readline().strip()
    #     #In thử dòng thứ 1 ra
    #     # print(header)
    #     #Tạo mảng chưa data học sinh
    #     data_hocsinh = []
    #     #Đọc dòng thứ 2
    #     row = f.readline().strip()
    #     #Nếu dòng thứ 2 khác rỗng thì
    #     while row != "":
    #         data_hocsinh.append(row) #Thêm dòng hiện hành vào mảng data học sinh
    #         row = f.readline().strip()  #Đọc dòng tiếp theo để kiểm tra
    #     #In mảng học sinh ra màn hình
    #     print(data_hocsinh)
    #     #Khởi tạo mảng tên
    #     mang_ten = []
    #     f.close()
    #     #Dùng vòng lặp for để xử lí tên
    #     for i in data_hocsinh:
    #         mang_tam = i.split(",")
    #         #Thêm tên hiển thị vào biến tên
    #         mang_ten.append(mang_tam[5])
    #
    #     #Khai báo biến tên và gán giá trị mảng tên vào
    #     names = mang_ten
    #     #Lấy số báo danh
    #     mang_so_bao_danh = load_numbers()
    #     print("Tới bước chọn camera")
    #     #In cam ra màn hình
    #     cam = cv2.VideoCapture(0)
    #     #set kích thước cam
    #     cam.set(3,640)
    #     cam.set(4,480)
    #     minW = 0.1 * cam.get(3)
    #     minH = 0.1 * cam.get(4)
    #     #Màu cơ bản
    #     #Màu vàng
    #     yellow = (255,255,0)
    #     pink = (255,0,255)
    #     red = (255,0,0)
    #     green = (0,255,0)
    #     i = 0
    #     # playsound("Audio/start.mp3")
    #     # print("Tới vòng lặp")
    #     while True:
    #         #Đọc cam
    #         # print("Bước đọc Camera")
    #         ret,frame = cam.read()
    #         # print("Đã đọc dữ liệu của camera")
    #         #Chỉnh sửa kích thước ảnh
    #         frame = cv2.resize(frame,(600,300))
    #         # Lấy kích thước ảnh
    #         height, width = frame.shape[:2]
    #         # Tính toán vị trí chia ảnh thành hai phần
    #         split_point = width // 2
    #         # Chia ảnh thành hai phần
    #         left_image = frame[:, :split_point]
    #         right_image = frame[:, split_point:]
    #         image_draw = frame
    #         #Lấy tên từ khuôn mặt
    #         # print('Tới bước lấy dữ liệu khuôn mặt')
    #         khuon_mat = load_face(right_image,names,minW,minH,font,recognizer,faceCascade)
    #         #Lấy ID từ khuôn mặt
    #         # print("Tới bước lấy ID từ khuôn mặt")
    #         so_bao_danh = load_faces_numbers(right_image,mang_so_bao_danh,minW,minH,recognizer,faceCascade)
    #         # print("Số báo danh học sinh là",so_bao_danh)
    #         mang_du_lieu = return_data_in_list(so_bao_danh)
    #         # print("Tới bước đọc dữ liệu trong mã QR")
    #         if mang_du_lieu[0] != "":
    #             print("Có khuôn mặt")
    #             list_data_qr = return_list_qr_data(left_image,dectector)
    #         else:
    #             print("Không có khuôn mặt")
    #             list_data_qr = ""
    #
    #
    #         #Tạo điều kiện
    #         #Nhận được dữ liệu
    #         if len(list_data_qr) != 0:
    #             thongtin = list_data_qr.split(",")
    #             self.signal_data.emit(thongtin)
    #             #Nhận dữ liệu của khuôn mặt và mã qr
    #             if len(thongtin) != 0 and len(mang_du_lieu) != 0 and thongtin[1] == mang_du_lieu[1]:
    #                 playsound("Audio/Dang_xac_nhan.mp3")
    #                 print("Dữ liệu trong mã qr là",thongtin)
    #                 print("Dữ liệu khuôn mặt là",mang_du_lieu)
    #                 thoi_gian = datetime.datetime.now()
    #                 ngay = thoi_gian.day
    #                 thang = thoi_gian.month
    #                 nam = thoi_gian.year
    #                 gio = thoi_gian.hour
    #                 phut = thoi_gian.minute
    #                 giay = thoi_gian.second
    #                 thoigian = f"{gio}:{phut}:{giay}"
    #                 buoi = ""
    #                 if gio <= 12:
    #                     buoi = "morning"
    #                 else:
    #                     buoi = "afternoon"
    #
    #
    #                 truong = xu_li_ten_truong(thongtin[2])
    #                 lop = thongtin[3]
    #                 print("Trường là",truong)
    #                 print("Lớp là",lop)
    #                 if truong != "levantam" and truong != "maithanhthe" and truong != "vinhloi" \
    #                     and truong != "nguyendu" and truong != "tranvanbay":
    #                     truong = "truongkhac"
    #                 else:
    #                     pass
    #                 f = open(f"Time_setup/{truong}_{lop}_{buoi}.txt",mode = "r",encoding="utf-8-sig")
    #                 tg = f.readline().split(",")
    #                 print("Thời gian là",tg)
    #                 f.close()
    #                 gio_thoi_gian = int(tg[0])
    #                 phut_thoi_gian = int(tg[1])
    #
    #                 print(f"Giờ điểm danh là:{gio}:{phut}")
    #                 print(type(gio))
    #                 if gio > 1 and gio < 12:
    #                     #Buổi sáng
    #                     if gio < gio_thoi_gian:
    #                         diem_danh = "Đúng giờ"
    #                     elif gio == gio_thoi_gian and phut <= phut_thoi_gian:
    #                         diem_danh = "Đúng giờ"
    #                     else:
    #                         diem_danh = "Đi trễ"
    #                 else:
    #                     if gio < gio_thoi_gian:
    #                         diem_danh = "Đúng giờ"
    #                     elif gio == gio_thoi_gian and phut <= phut_thoi_gian:
    #                         diem_danh = "Đúng giờ"
    #                     else:
    #                         diem_danh = "Đi trễ"
    #                 ngay_thang = f"{ngay}/{thang}/{nam}"
    #                 set_info_diem_danh_google_sheets_new(mang_du_lieu[0],mang_du_lieu[1],mang_du_lieu[3],mang_du_lieu[2],diem_danh,thoigian,ngay_thang)
    #                 playsound("Audio/Diem_danh_thanh_cong.mp3")
    #                 thongtin = ["","","","",""]
    #                 self.signal_data.emit(thongtin)
    #             #Trường hợp chỉ nhận mã qr mà không có thông tin khuôn mặt
    #             elif len(thongtin) != 0 and thongtin[1] != "" and len(mang_du_lieu) != 0 and mang_du_lieu[0] == "" :
    #                 thongtin = ["","","","",""]
    #                 self.signal_data.emit(thongtin)
    #             elif len(thongtin) != 0 and thongtin[1] != "" and len(mang_du_lieu) != 0 and \
    #                     ((thongtin[1] != mang_du_lieu[1]) or
    #                      (thongtin[0] != mang_du_lieu[0]) or (thongtin[3] != mang_du_lieu[2]) or
    #                      (thongtin[2] != mang_du_lieu[3])):
    #                 playsound("Audio/Khong_kop.mp3")
    #                 thongtin = ["","","","",""]
    #                 self.signal_data.emit(thongtin)
    #         else:
    #             pass


        #     #Vẽ 1 đường chia đôi màn hình chính
        #     cv2.line(image_draw,(300,0),(300,300),yellow,4)
        #     self.signal_main_far.emit(frame)
        #     self.signal1_op_far.emit(left_image)
        #     self.signal2_op_far.emit(khuon_mat)
        #
        #     list_data = []
        #     # cv2.imshow("Camera 1",left_image)
        #     # cv2.imshow("Camera 2",right_image)
        #     if self.gg == False:
        #         break
        # cam.release()
        # cv2.destroyAllWindows()