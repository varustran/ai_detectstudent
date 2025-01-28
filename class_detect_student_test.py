import cv2
from PyQt5.QtWidgets import QMessageBox
#
from def_important import *
import os
# #
import time
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QMutex, QWaitCondition
from imutils.video import VideoStream
# # from playsound import playsound
from xu_li_gian_lan import ghi_nhan_gian_lan
from DEF_NEW import *
#from gaze_tracking import GazeTracking
class live_stream(QThread):
    signal = pyqtSignal(np.ndarray)
    signal_ngung = pyqtSignal(object)
    signal_ket_thuc_audio = pyqtSignal(object)
    signal_khoi_dong_audio = pyqtSignal(object)
    signal_thong_bao = pyqtSignal(object)


    def __init__(self, index):
        super(live_stream, self).__init__()
        self.device = None
        # self.out_file = None
        self.classes = None
        # self.model = None
        self.gg = True
        self.player = None
        self.index = index
        self.kiemtra = []
        self.nhaclan1 = True
        self.nhaclan2 = True
        self.nhaclan3 = True
        self.dem = 0

    # Hàm chạy luồng
    def run(self):
        # print("run 1111")
        self.gg = True
        self.run_program()  # Hàm chạy chương trình chính

    # Hàm chạy chương trình
    def run_program(self):
        #playsound("bat_dau_vao_thi.mp3")
        print("Gửi tín hiệu từ class giám sát thường qua giám sát âm thanh")
        khoi_dong = "Bat"
        src = self.index
        self.signal_khoi_dong_audio.emit(khoi_dong)
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)
        mp_drawing = mp.solutions.drawing_utils
        drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(215, 215, 215))
        #gaze = GazeTracking()
        cap = VideoStream(src=self.index).start()
        print("Khởi động")
        print(src)
        # kiem_tra_du_lieu = open("Kiem_tra_luong_chay/kiem_tra.txt","r")
        # Kiem_Tra = kiem_tra_du_lieu.readline().strip()
        # kiem_tra_du_lieu.close()
        kiem_tra_che_cam = 0
        so_lan_nhac_che_camera = 0
        gioi_han_che_cam = 0
        ghi_du_phong = 0
        am_thanh = 0
        # ai_ear = speech_recognition.Recognizer() # nghe người dùng nói
        # you = "" # Lời nói người dùng
        # with speech_recognition.Microphone() as mic:
        #     audio = ai_ear.record(mic, duration = 5)
        #     try:
        #         you = ai_ear.recognize_google(audio, language = 'vi-VN')
        #         print(you)
        #     except:
        #         pass
        while True:

            frame = cap.read()  # Đọc dữ l
            src = self.index
            # iệu camera
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Chuyển đồi màu ảnh
            image.flags.writeable = False  # Gắn cờ sai
            results = face_mesh.process(image)  # Trả về kết quả nhận dạng
            image.flags.writeable = True  # Gắn cờ đúng cho ảnh
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Chuyển đổi màu ảnh
            img_h, img_w, img_c = image.shape  # Lấy kích thước hình dạng ảnh
            face_3d = []  # Tạo mảng 3 chiều
            face_2d = []  # Tạo mảng 2 chiều
            text = ""  # Biến ghi hành động

            ghi_du_phong += 1
            if ghi_du_phong == 1:
                cv2.imwrite("Picture/anh_du_phong.png", frame)
            else:
                pass
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    for idx, lm in enumerate(face_landmarks.landmark):
                        if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                            if idx == 1:
                                nose_2d = (lm.x * img_w, lm.y * img_h)
                                nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)
                            x, y = int(lm.x * img_w), int(lm.y * img_h)
                            face_2d.append([x, y])
                            face_3d.append([x, y, lm.z])
                    face_2d = np.array(face_2d, dtype=np.float64)
                    face_3d = np.array(face_3d, dtype=np.float64)
                    focal_length = 1 * img_w
                    cam_matrix = np.array([[focal_length, 0, img_h / 2],
                                           [0, focal_length, img_w / 2],
                                           [0, 0, 1]])
                    dist_matrix = np.zeros((4, 1), dtype=np.float64)
                    success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
                    rmat, jac = cv2.Rodrigues(rot_vec)
                    angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)
                    x = angles[0] * 360
                    y = angles[1] * 360
                    z = angles[2] * 360
                    gia_tri_gian_lan_trai = 0
                    gia_tri_gian_lan_phai = 0
                    if y < -11:

                            if x > 34:
                                text = "Dang ngua len"
                            elif y < -11:
                                text = "Trai"
                                #self.kiemtra.append(1)
                                if y < -11:
                                    text = "Trai"
                                    if y < -11:
                                        text = "Trai"
                                        if y < -11:
                                            text = "Trai"
                                            self.kiemtra.append(1)
                    elif y > 11:
                            
                            if x > 34:
                                text = "Dang ngua len"
                            elif y > 11:
                                text = "Phai"
                                #self.kiemtra.append(1)
                                if y > 11:
                                    text = "Phai"
                                    if y > 11:
                                        text = "Phai"
                                        if y > 11:
                                            text = "Phai"
                                            self.kiemtra.append(1)
                    elif x < 4:
                        text = "Dang lam bai"
                    elif x > 10:
                        text = "Dang ngua len"
                    else:
                        text = "Nhin thang"
                    nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix,
                                                                     dist_matrix)
                    p1 = (int(nose_2d[0]), int(nose_2d[1]))
                    p2 = (int(nose_2d[0] + y * 10), int(nose_2d[1] - x * 10))
                    cv2.line(image, p1, p2, (139, 0, 0), 2)
                    cv2.circle(image, p1, 8, (0, 0, 139), -1)
                    cv2.circle(image, p2, 8, (0, 0, 139), -1)
                    cv2.putText(image, text, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                    # cv2.putText(image, "X:  " + str(x), (20, 130), cv2.FONT_HERSHEY_DUPLEX, 1,
                    #             (0, 0, 255), 1)
                    # cv2.putText(image, "Y:  " + str(y), (20, 165), cv2.FONT_HERSHEY_DUPLEX, 1,
                    #             (0, 0, 255), 1)
                    cv2.putText(image, "SO CAMERA:  " + str(src), (200, 400), cv2.FONT_HERSHEY_DUPLEX, 1,
                                (153, 204, 0), 1)

                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=drawing_spec,
                    connection_drawing_spec=drawing_spec)

                # print(text)
                # Hàm thuật tính toán
                tong_loi = sum(self.kiemtra)
                # Kiểm tra lỗi
                # Nhắc nhở lần 1
                if tong_loi > 50 and tong_loi < 100:
                    if self.nhaclan1 == True:
                        # print("Gửi tín hiệu nhắc nhở 1")
                        ngung_am_thanh = "Dung"
                        self.signal_ngung.emit(ngung_am_thanh)
                        #self.signal_thong_bao.emit(1)
                        self.nhaclan1 = False
                        cv2.imwrite("Picture/bangchung.png", frame)
                        cv2.imwrite("Picture/anh_frame.png", image)
                        send_photos()
                        send_file_text()

                    else:
                        pass
                elif tong_loi > 100 and tong_loi < 150:
                    if self.nhaclan2 == True:
                        print("Gửi tín hiệu nhắc nhở 2")
                        ngung_am_thanh = "Dung"
                        self.signal_ngung.emit(ngung_am_thanh)
                        #self.signal_thong_bao.emit(2)
                        self.nhaclan2 = False
                        cv2.imwrite("Picture/bangchung.png", frame)
                        cv2.imwrite("Picture/anh_frame.png", image)
                        send_photos()
                        send_file_text()
                    else:
                        pass

                elif tong_loi > 200:
                    self.signal_thong_bao.emit(3)
                    ngung_am_thanh = "Dung"
                    self.signal_ngung.emit(ngung_am_thanh)
                    dung_audio = "Dung"

                    print("Học sinh gian lận")

                    cv2.imwrite("Picture/bangchung.png", frame)
                    cv2.imwrite("Picture/anh_frame.png", image)
                    # # Gửi hình ảnh đi
                    # print("Tới bước gửi ảnh đi")
                    send_photos()
                    # Gửi file nội dung đi
                    # print("Tới bước gửi nội dung đi")
                    send_file_text()
                    self.signal_ket_thuc_audio.emit(dung_audio)
                    #Ghi nhận gian lan
                    # print("Tới bước ghi gian lận")
                    ghi_nhan_gian_lan()
                    ghi_nhan_gian_lan()
                    ghi_du_phong = 0
                    # Dừng camera
                    tong_loi = 0
            else:
                kiem_tra_che_cam += 1
                if kiem_tra_che_cam > 55:
                    # print("Đang che camera")
                    so_lan_nhac_che_camera += 1
                    kiem_tra_che_cam = 0
                    # if so_lan_nhac_che_camera == 1:
                    #     # print("Đã gửi tín hiệu đi che cam lần 1")
                    #     ngung_am_thanh = "Dung"
                    #     self.signal_thong_bao.emit(4)
                    #     self.signal_ngung.emit(ngung_am_thanh)
                    #     cv2.imwrite("Picture/bangchung.png", frame)
                    #     send_photos_che_cam
                    #     send_file_text()
                    #     time.sleep(1)
                    #
                    # elif so_lan_nhac_che_camera == 2:
                    #     # print("Đã gửi tín hiệu đi che cam lần 2")
                    #     ngung_am_thanh = "Dung"
                    #     self.signal_thong_bao.emit(5)
                    #     self.signal_ngung.emit(ngung_am_thanh)
                    #     cv2.imwrite("Picture/bangchung.png", frame)
                    #     # cv2.imwrite("Picture/anh_frame.png", image)
                    #     send_photos_che_cam
                    #     send_file_text()
                    #     time.sleep(1)
                    #     # QMessageBox.information(self, "Nhắc nhở vi phạm", "Thí sinh vui lòng không che camera (Lần 2)")
                    # elif so_lan_nhac_che_camera == 3:
                    #     self.signal_thong_bao.emit(6)
                    #     ngung_am_thanh = "Dung"
                    #     self.signal_ngung.emit(ngung_am_thanh)
                    #     cv2.imwrite("Picture/bangchung.png", frame)
                    #     # cv2.imwrite("Picture/anh_frame.png", image)
                    #     dung_audio = "Dung"
                    #     self.signal_ket_thuc_audio.emit(dung_audio)
                    #     time.sleep(1)
                    #     # QMessageBox.information(self, "Thông báo vi phạm", "Hệ thống xác nhận bạn đã vi phạm quy chế thi")
                    #     # # Gửi hình ảnh đi
                    #     # print("Tới bước gửi ảnh đi")
                    #     send_photos_che_cam
                    #     #send_photos_du_phong()
                    #     ghi_nhan_che_cam()
                    #     # Gửi file nội dung đi
                    #     # print("Tới bước gửi ảnh và thông tin đi")
                    #     send_file_text()
                    #     ghi_du_phong = 0
                    #     break

            # Trả dữ liệu hình ảnh
            self.signal.emit(image)
            if self.gg == False:
                dung = "Dung"
                self.signal_ket_thuc_audio.emit(dung)
                break
        cap.stop()  # Dừng camera

    # Hàm dừng chương trình
    def stop(self):
        self.gg = False
        self.wait()
        cv2.destroyAllWindows()  # Huỷ cửa sổ Camera
        self.terminate()
    # Hàm cho điều kiện While True sai
    def pause_stream(self):
        #self.gg = False
        pass