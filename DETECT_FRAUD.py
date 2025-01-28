import subprocess
import re
import nmap
import os
import sys
import time

# from upload import upload_image_qr
import gspread
# import pyperclip as pyperclip
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QMutex, QWaitCondition
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QCompleter, QMessageBox, QLineEdit
# from def_important import *
# import datetime
# from xoa_tieng_viet import no_accent_vietnamese
from layout_new import Ui_MainWindow
# from class_make_data import attendance_face
from class_detect_student_test import live_stream
from class_attendance_qr_code import Attendance_qr_class
from class_detect_face import detect_face_class
from class_detect_far import detect_far, CameraDetectionThread
# from PIL import Image
from class_detect_audio import detect_audio
from def_important import *
from class_provide_camera import *
# import telegram
# from playsound import *
#hàm chỉnh ảnh ở camera chính
a_nguoi = 0
def convert_cv_qt_camera_main(cv_img):
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    p = convert_to_Qt_format.scaled(300, 150, Qt.KeepAspectRatio)  # (Cao, rộng)
    return QPixmap.fromImage(p)

#Hàm chỉnh ảnh ở camera 1 (Test)
def convert_cv_qt_camera_1_test(cv_img):
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    p = convert_to_Qt_format.scaled(300, 300, Qt.KeepAspectRatio)  # (Cao, rộng)
    return QPixmap.fromImage(p)

#Hàm chỉnh ảnh ở camera 1
def convert_cv_qt_camera_1(cv_img):
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    p = convert_to_Qt_format.scaled(300, 300, Qt.KeepAspectRatio)  # (Cao, rộng)
    return QPixmap.fromImage(p)

#Hàm chỉnh ảnh ở camera 2
def convert_cv_qt_camera_2(cv_img):
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    p = convert_to_Qt_format.scaled(300, 300, Qt.KeepAspectRatio)  # (Cao, rộng)
    return QPixmap.fromImage(p)

# Hàm chuyển đổi cho màn hình giám sát từ xa
def convert_cv_qt_far(cv_img):
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    p = convert_to_Qt_format.scaled(550, 491, Qt.KeepAspectRatio)  # (Cao, rộng)
    return QPixmap.fromImage(p)


# Hàm chuyển đổi ảnh thông thường sang ảnh phù hợp với QT5
def convert_cv_qt(cv_img):
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    p = convert_to_Qt_format.scaled(421, 331, Qt.KeepAspectRatio)
    return QPixmap.fromImage(p)


# Hàm chuyển đổi khi qua điểm danh bằng mã QR
def convert_cv_qt_attendance(cv_img):
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    p = convert_to_Qt_format.scaled(500, 381, Qt.KeepAspectRatio)
    return QPixmap.fromImage(p)

#Dạ đaây a
def convert_cv_qt_make_data(cv_img):
    """Convert from an opencv image to QPixmap"""
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    p = convert_to_Qt_format.scaled(421, 430, Qt.KeepAspectRatio)
    return QPixmap.fromImage(p)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # the way app working
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("Image/logo_hk_rm.png"))
        self.setWindowTitle("Giám Thị AI")



        #Qua màn hình giám thị lựa chọn
        #self.uic.btn_tao_test_return.clicked.connect(self.display_tao_xem)

        #Qua màn hình tạo bài kiểm tra
        # self.uic.btn_tao_bai_kiem_tra.clicked.connect(self.display_creat_test_new)

        #Nút từ màn hình tạo bài kiểm tra, xem kết quả về màn hình giám thị
        # self.uic.btn_giam_thi_test_return.clicked.connect(self.display_giam_thi_new)


        #Nút qua màn hình lựa chọn kiểm tra của giám thị
        # self.uic.btn_kiem_tra_gt_new.clicked.connect(self.display_chose_giam_thi)


        #Nút thoát ở màn hình lựa chọn giám sát
        self.uic.btn_giam_sat_close.clicked.connect(self.close)

        #Nút từ màn hình học sinh điểm danh qua menu điểm danh
        self.uic.btn_menu_diem_danh.clicked.connect(self.display_menu_diem_danh_new)

        #Nút từ màn hình điểm danh, tạo dữ liệu qua màn hình lựa chọn tạo dữ liệu
        self.uic.btn_menu_tao_du_lieu.clicked.connect(self.display_menu_tao_du_lieu_new)

        #Nút từ màn hình menu tạo dữ liệu sang màn hình điểm danh, tạo dữ liệu
        self.uic.btn_tao_du_lieu_return.clicked.connect(self.display_menu_tao_du_lieu_return)

        #Nút từ màn hình tiện ích học sinh qua màn hình kiểm tra kiến thức
        # self.uic.btn_kiem_tra.clicked.connect(self.display_kiem_tra_kien_thuc)
        # #Nút từ màn hình kiểm tra kiến thức trở về màn hình tiện ích
        # self.uic.btn_type_test_return.clicked.connect(self.display_tien_ich)
        # #Nút thoát ở màn hình kiểm tra kiến thức
        # self.uic.btn_type_test_close.clicked.connect(self.close)
        # #Nút phiếu trả lời trắc nghiệm
        # self.uic.btn_type_test_40.clicked.connect(self.display_lam_bai_kiem_tra)
        #
        #
        # #Nút từ màn hình kiẻm tra trắc nghiệm trở về màn hình lựa chọn
        # self.uic.btn_type_test_40_return.clicked.connect(self.display_kiem_tra_kien_thuc)
        # #Nút xem hướng dẫn làm bài
        # self.uic.btn_type_huong_dan.clicked.connect(self.view_huong_dan)






        #Mặc định camera
        self.uic.input_attendance_face_cam.setText("0")
        #Khởi động micro
        # start_micro()

        #Set ảnh cho màn hình giám sát rộng
        self.uic.screen_main.setPixmap(QPixmap("Image/main_screen.png"))
        self.uic.screen_main.setScaledContents(True)
        #Set thí sinh 1
        self.uic.screen_1.setPixmap(QPixmap("Image/TS_1.png"))
        self.uic.screen_1.setScaledContents(True)
        #Set thí sinh 2
        self.uic.screen_2.setPixmap(QPixmap("Image/TS_2.png"))
        self.uic.screen_2.setScaledContents(True)




        #Nút từ màn hình điểm danh, tạo dữ liệu, thiết lập thời gian sang màn hình thiết lập thời gian
        self.uic.btn_menu_thiet_lap_time.clicked.connect(self.display_setup_time)



        #Nút thoát
        self.uic.btn_tao_du_lieu_close.clicked.connect(self.close)
        #
        self.uic.btn_diem_danh_menu_close.clicked.connect(self.close)


        #Nút từ màn hình lựa chọn trong điểm danh sang màn hình học sinh
        self.uic.btn_diem_danh_menu_return.clicked.connect(self.display_menu_diem_danh_return)


        #Set ảnh chỗ xoá qr

        self.uic.input_screen_image_2.setPixmap(QPixmap("Image/take_qr.jpg"))
        self.uic.input_screen_image_2.setScaledContents(True)

        #Set ảnh cho màn hình điểm danh
        self.uic.screen_attendance_main.setPixmap(QPixmap("Image/main_screen.png"))
        self.uic.screen_attendance_main.setScaledContents(True)
        #Set thí sinh 1
        self.uic.screen_attendance_1.setPixmap(QPixmap("Image/QR.png"))
        self.uic.screen_attendance_1.setScaledContents(True)
        #Set thí sinh 2
        self.uic.screen_attendance_2.setPixmap(QPixmap("Image/KM.png"))
        self.uic.screen_attendance_2.setScaledContents(True)
        #Vô hiệu hoá nút tạm dừng trong điểm danh
        self.uic.btn_attendance_far_stop.setEnabled(False)

        #Set ảnh cho màn hình giám sát
        #Đưa hình lên camera giám sát
        self.uic.screen_detec_camera.setPixmap(QPixmap("Image/camera_screen.png"))
        self.uic.screen_detec_camera.setScaledContents(True)
        #Đưa ảnh lên màn hình điểm danh bằng mã qr
        self.uic.btn_attendance_camera.setPixmap(QPixmap("Image/camera_screen.png"))
        self.uic.btn_attendance_camera.setScaledContents(True)
        #Đưa ảnh lên camera
        self.uic.input_camera_make_data.setPixmap(QPixmap("Image/camera_dai.png"))
        self.uic.input_camera_make_data.setScaledContents(True)
        #Dua ảnh lên màn hình điểm danh khuôn mặt
        self.uic.input_camera_attendance_face.setPixmap(QPixmap("Image/camera_dai.png"))
        self.uic.input_camera_attendance_face.setScaledContents(True)
        #Đưa ảnh lên giám sát rộng
        self.uic.input_detect_far_camera.setPixmap(QPixmap("Image/bia_zalo.png"))
        self.uic.input_detect_far_camera.setScaledContents(True)
        # Khoá nút X
        # Thiết lập cờ để hiển thị nút X trên cửa sổ
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        # Tạo luồng
        self.thread = {}
        a = self.uic.input_detec_name.text()
        # MENU CHÍNH
        # Khai báo các nút ở menu chính
        # Nút từ màn hình menu chính qua màn hình học sinh
        self.uic.btn_menu_student.clicked.connect(self.display_student)
        # Nút từ màn hình menu chính qua màn hình xác nhận điểm danh
        self.uic.btn_menu_teacher.clicked.connect(self.display_teacher)
        # Nút thoát trong màn hình menu chính
        self.uic.btn_menu_close_main.clicked.connect(self.close)
        #Nút mở trang chủ detect fraud
        self.uic.btn_detect_fraud.clicked.connect(self.open_trang_chu_detect_fraud)
        #Nút mở trang chủ detect fraude




        #Nút enable các nút
        #Nút chuẩn bị
        self.uic.btn_detect_far_ready.setEnabled(False)
        #Nút bắt đầu
        self.uic.btn_detect_far_start_detect_new.setEnabled(False)
        #Nút dừng
        self.uic.btn_detect_far_stop.setEnabled(False)



        #MÀN HÌNH LỰA CHỌN CHẾ ĐỘ GIÁM SÁT
        self.uic.btn_giam_sat_menu.clicked.connect(self.display_menu_giam_sat_return)
        #Nút thoát
        self.uic.btn_hoc_sinh_close.clicked.connect(self.close)


        # MÀN HÌNH HỌC SINH
        # Khai báo các nút ở màn hình học sinh
        # Nút từ màn hình học sinh qua màn hình giám sát
        self.uic.btn_menu_detec.clicked.connect(self.qt_display_detec)

        # Nút từ màn hình học sinh qua màn hình giám sát rộng
        self.uic.btn_menu_dectect_far.clicked.connect(self.display_giam_sat_rong)

        #Nút từ màn hình học sinh sang mà hình điểm danh bằng khuôn mặt
        # self.uic.btn_menu_attendance_khuon_mat.clicked.connect(self.display_diem_danh_khuon_mat)

        #Nút từ màn hình học sinh qua màn hình giám sát 2 người
        self.uic.btn_menu_dectect_two_peo.clicked.connect(self.display_detect_far)
        # Nút từ màn hình học sinh qua màn hình điểm danh
        self.uic.btn_menu_attendance.clicked.connect(self.qt_display_attendance)
        # Nút từ màn hình học sinh về màn hình trang chủ
        self.uic.btn_hoc_sinh_return.clicked.connect(self.qt_display_menu)
        # Nút thoát trong màn hình học sinh
        self.uic.btn_hoc_sinh_close.clicked.connect(self.close)
        #Nút qua màn hình tiện ích
        # self.uic.btn_menu_mini.clicked.connect(self.display_tien_ich)
        #Nút từ màn hình học sinh qua màn hình giám sát menu
        self.uic.btn_menu_giam_sat.clicked.connect(self.display_giam_sat_new)




        #MÀN HÌNH GIÁM SÁT
        #Khai báo các thành phần ở màn hình giám sát
        # Nút bắt đầu thực hiện giám sát
        self.uic.btn_detec_start.clicked.connect(self.start_detect)
        # Nút trích xuất dữ liệu (mở thư mục chính thông tin học sinh)
        #self.uic.btn_detec_kt_thong_tin.clicked.connect(self.open_folder_giam_sat)
        # Nút lưu thông tin học sinh vừa nhập
        self.uic.btn_detec_export.clicked.connect(self.make_file_txt)
        # Nút hoàn thành bài thi
        self.uic.btn_detec_finish.clicked.connect(self.hoan_thanh_bai_thi)
        # Nút xoá nội dung trong form thông tin ở màn hình giám sát
        self.uic.btn_detec_clear_content.clicked.connect(self.clear_man_hinh)
        # Nút mở thư mục chứa file token và ID của BOT mail
        # self.uic.btn_detec_bot_telegram.clicked.connect(self.open_token_txt)
        # Nút thoát ở màn hình giám sát
        self.uic.btn_detec_close.clicked.connect(self.close_giam_sat)
        # Nút từ màn hình giám sát trở về màn hình học sinh
        self.uic.btn_detect_menu_return.clicked.connect(self.display_student_return)
        #Nút từ màn hình giám sát qua màn hình bot email
        self.uic.btn_detec_bot_telegram.clicked.connect(self.display_bot_email)
        #Vô hiệu hoá nút bắt đầu
        self.uic.btn_detec_start.setEnabled(False)
        #Vô hiệu hoá nút hoàn thành
        self.uic.btn_detec_finish.setEnabled(False)
        #Nút qua màn hình môn học
        self.uic.btn_select_subject.clicked.connect(self.display_subject)
        #Nút trở về màn hình giám sát
        self.uic.btn_subject_return.clicked.connect(self.display_giam_sat)
        #Nút lựa chọn môn học
        type_subject = ["Toán","KHTN","Tin học","Ngữ văn","Lịch sử","Địa lí","GDCD","Tiếng anh","Mĩ thuật","Âm nhạc","Thể dục"]
        #Tạo đối tượng
        completer_type = QCompleter(type_subject,self.uic.input_detec_subject)
        # Thiết lập QCompleter cho QLineEdit
        self.uic.input_detec_subject.setCompleter(completer_type)



        # #Nút bật khả năng truy cập micro
        # self.uic.btn_detec_kt_truy_cap.clicked.connect(self.detect_audio_on)
        # #Nút tắt khả năng truy cập
        # self.uic.btn_detec_kt_truy_cap_close.clicked.connect(self.detect_audio_off)




        #MÀN HÌNH ĐIỂM DANH
        #Khai báo một số nút ở màn hình điểm danh
        # Từ màn hình điểm danh sang màn hình điểm danh bằng mã QR
        # self.uic.btn_menu_attendance_qr.clicked.connect(self.qt_diplay_attendance_qr)
        # Từ màn hình điểm danh sang màn hình điểm danh bằng khuôn mặt
        # self.uic.btn_menu_attendance_face.clicked.connect(self.qt_diplay_attendance_face)
        # Nút từ màn hình điểm danh trở về màn hình học sinh
        self.uic.btn_menu_attendance_return.clicked.connect(self.display_diem_danh)
        # Nút thoát ở màn hình điểm danh
        self.uic.btn_menu_attendance_close.clicked.connect(self.close)
        #Nút chuyển qua màn hình thiết đặt thời gian
        # self.uic.btn_menu_setup_time.clicked.connect(self.display_setup_time)



        #MÀN HÌNH ĐIỂM DANH BẰNG MÃ QR
        #Khai báo các nút ở màn hình điểm danh bằng mã QR
        # Nút từ màn hình điểm danh bằng mã QR sang màn hình tạo mã QR
        self.uic.btn_attendance_make_qr_data.clicked.connect(self.qt_display_make_data_qr)
        # Nút từ màn hình điểm danh bẳng mã qr vào màn hình điểm danh (Mã QR)
        self.uic.btn_attendance_as_qr_code.clicked.connect(self.qt_display_attendance_qr)
        # Nút mở thư mục để kiểm tra danh sách học sinh điểm danh bằng mã QR
        self.uic.btn_attendance_show_list_qr.clicked.connect(self.open_folder_excel_qr)
        # Nút từ màn hình điểm danh bằng mã QR trở về màn hình điểm danh
        self.uic.btn_menu_attendance_qr_return.clicked.connect(self.qt_display_attendance_qr_return)
        #Nút thoát ở màn hình điểm danh bằng mã QR
        self.uic.btn_menu_attendance_qr_close.clicked.connect(self.close)






        #MÀN HÌNH TẠO MÃ QR
        #Khai báo các nút ở màn hình tạo mã QR
        # Nút từ màn hình tạo mã QR trở lại màn hình menu điểm danh bằng mã QR
        self.uic.btn_attendance_qr_return.clicked.connect(self.display_menu_tao_du_lieu_new)
        # Nút lưu mã QR và gửi đến kênh chat telegram
        self.uic.btn_data_save.clicked.connect(self.save_qr_send)
        # Nút xoá dữ liệu ở màn hình tạo mã QR
        self.uic.btn_make_data_qr_clear.clicked.connect(self.clear_data_in_make_qr)
        # Nút mở thư mục BOT QR
        self.uic.btn_detec_bot_telegram_qr.clicked.connect(self.open_qr_bot)
        # Nút thoát khỏi chương trình ở màn hình tạo mã QR
        self.uic.btn_attendance_qr_close.clicked.connect(self.close)

        #MÀN HÌNH ĐIỂM DANH BẰNG MÃ QR
        #Khai báo một số nút ở màn hình điểm danh bằng mã QR
        # Nút từ màn hình điểm danh bằng mã qr về menu điểm danh bằng mã qr
        self.uic.btn_attendance_qr_detect_return.clicked.connect(self.qt_display_attendance_qr_menu_return)
        # Nút thoát màn hình điểm danh bằng mã qr
        self.uic.btn_attendance_qr_detect_close.clicked.connect(self.close)
        # Nút điểm danh bằng mã QR
        self.uic.btn_attendance_checked.clicked.connect(self.start_qr)
        #Nút dừng camera
        self.uic.btn_attendance_qr_stop.clicked.connect(self.stop_camera_qr)


        # MÀN HÌNH ĐIỂM DANH BẰNG KHUÔN MẶT
        #Khai báo ột số nút điểm danh bằng khuôn mặt
        # Nút từ màn hình menu điểm danh bằng khuôn mặt sang màn hình tạo dữ liệu khuôn mặt
        # self.uic.btn_attendance_make_face_data.clicked.connect(self.qt_display_attendance_make_data_face)
        # # Nút từ màn hình menu điểm danh bằng khuôn mặt sang màn hình cập nhật dữ liệu khuôn mặt
        # # self.uic.btn_attendance_update_data.clicked.connect(self.qt_display_attendance_update_data_face)
        # # Nút từ menu điểm danh bằng khuôn mặt sang màn hình điểm danh bằng khuôn mặt
        # self.uic.btn_attendance_as_face.clicked.connect(self.qt_display_attendance_face)
        # # Nút mở danh sách điểm danh bằng khuôn mặt
        # self.uic.btn_attendance_show_list_face.clicked.connect(self.open_folder_excel_face)
        # # Nút từ menu điểm danh bằng khuôn mặt trở về màn hình menu điểm danh
        # self.uic.btn_menu_attendance_face_return.clicked.connect(self.qt_display_attendance_menu_return)
        # # Nút thoát ở màn hình điểm danh bằng khuôn mặt
        # self.uic.btn_menu_attendance_face_close.clicked.connect(self.close)
        # #Nút xoá màn hình ở điểm danh bằng khuôn mặt
        # self.uic.btn_attendance_face_cam_clear.clicked.connect(self.clear_content_attendance_face)

        #TẠO DỮ LIỆU KHUÔN MẶT
        # # Nút từ màn hình tạo dữ liệu khuôn mặt trở về màn hình menu điểm danh bằng khuôn mặt
        # self.uic.btn_make_data_face_menu.clicked.connect(self.qt_display_make_data_face_return)
        # # Nút mở thư mục ảnh
        # self.uic.btn_show_folder_face.clicked.connect(self.show_folder_img_face)
        # # Nút thoát trong tạo dữ liệu khuôn mặt
        # self.uic.btn_make_data_face_close.clicked.connect(self.close)
        # # Tạo dữ liệu khuôn mặt
        # self.uic.btn_make_face_data.clicked.connect(self.start_make_data_face)
        # # Nút trích xuất dữ liệu khuôn mặt
        # self.uic.btn_export_face_data.clicked.connect(self.make_data_export_data)
        # #Nút xoá content
        # self.uic.btn_data_input_clear.clicked.connect(self.make_data_face_clear_content)
        # #Nút lựa chọn dữ liệu
        # self.uic.btn_data_input.clicked.connect(self.make_data_link)




        # CẬP NHẬT DỮ LIỆU KHUÔN MẶT
        #Khai báo các nút ở màn hình cập nhật dữ liệu
        # Nút trở về màn hình cập nhật dữ liệu khuôn mặt
        # self.uic.btn_attendance_update_data_return.clicked.connect(self.attendance_update_data_return)
        # # Nút thoát chương trình ở màn hình cập nhật dữ liệu
        # self.uic.btn_attendance_update_data_close.clicked.connect(self.close)
        # # Nút cập nhật dữ liệu
        # self.uic.btn_update_data.clicked.connect(self.update_data_face)
        # # Nút mở xem file model
        # self.uic.btn_show_data_model.clicked.connect(self.show_folder_model)


        #ĐIỂM DANH BẰNG KHUÔN MẶT
        #Khai báo các nút ở màn hình đó
        # Nút trở về màn hình điểm danh khuôn mặt
        #self.uic.btn_attendance_face_return.clicked.connect(self.qt_display_attendance_qr_return)
        # Nút thoát
        # self.uic.btn_attendance_face_close.clicked.connect(self.close)
        # # Nút điểm danh bằng khuôn mặt
        # self.uic.btn_attendance_face_diemdanh.clicked.connect(self.start_detect_face)
        # # Nút xác nhận dữ liệu khuôn mặt của học sinh
        # # self.uic.btn_xacnhan_face.clicked.connect(self.xac_nhan_face)
        # # Chọn đường link cam nhận dạng
        # self.uic.btn_attendance_face_cam.clicked.connect(self.link_face_detect)
        # #Vô hiệu hoá nút dừng
        # self.uic.btn_attendance_face_cam_stop.setEnabled(False)
        # #Nút dừng camera
        # self.uic.btn_attendance_face_cam_stop.clicked.connect(self.stop_camera_attendance_face)









        #MÀN HÌNH XÁC NHẬN GIÁM THỊ
        #Khai báo một số nút ở màn hình xác nhận giám thị
        # Nút từ màn hình xác nhận trở về màn hình menu
        self.uic.btn_xac_nhan_gt_return.clicked.connect(self.qt_display_menu)
        # Nút thoát trong màn hình xác nhận
        self.uic.btn_xac_nhan_giam_thi_close.clicked.connect(self.close)
        # Nút xác nhận mã giám thị
        self.uic.btn_verification_tick.clicked.connect(self.verification_teacher)

        #MÀN HÌNH GIÁM THỊ
        #Khai báo một số nút ở màn hình giám thị
        # Nút từ màn hình giám thị qua màn hình đăng kí tài khoản
        self.uic.btn_giam_thi_dang_ki.clicked.connect(self.display_dang_ki_tai_khoan)
        # Nút qua màn hình đăng nhập
        self.uic.btn_giam_thi_dang_nhap.clicked.connect(self.display_dang_nhap_tk)
        # Nút từ màn hình giám thị trở về màn hình xác nhận
        self.uic.btn_giam_thi_return.clicked.connect(self.display_xac_nhan)
        # Nút thoát trong màn hình giám thị
        self.uic.btn_giam_thi_close.clicked.connect(self.close)
        #Nút qua màn hình quét điện thoại
        self.uic.btn_quet_dt.clicked.connect(self.display_quet_dien_thoai)
        #Nút từ màn hình quét điện thoại sang màn hình giám thị
        self.uic.btn_quet_dien_thoai_return.clicked.connect(self.display_quet_dien_thoai_return)


        #MÀN HÌNH ĐĂNG KÍ TÀI KHOẢN
        #Khai báo một số nút ở màn hình đăng kí tài khoản
        # Nút từ màn hình đăng kí trở về màn hình giám thị
        self.uic.btn_dang_ki_return.clicked.connect(self.display_giam_thi)
        # Nút thoát trong màn hình đăng kí tài khoản
        self.uic.btn_dang_ki_close.clicked.connect(self.close)
        # Nút đăng kí tài khoản
        self.uic.btn_dang_ki_start.clicked.connect(self.dang_ki_tai_khoan)
        #Nút xoá nội dung vừa viết
        self.uic.btn_dang_ki_clear.clicked.connect(self.clear_screen_dang_ki)




        #MÀN HÌNH ĐĂNG NHẬP
        #Khai báo một số nút ở màn hình đăng nhập
        # Nút từ màn hình đăng nhập trở về màn hình giám thị
        self.uic.btn_dang_nhap_return.clicked.connect(self.display_giam_thi)
        # Nút quên mật khẩu trong màn hình đăng nhập
        self.uic.btn_dang_nhap_quen_mk.clicked.connect(self.quen_mat_khau)
        # Nút đăng nhập tài khoản
        self.uic.btn_dang_nhap_tai_khoan.clicked.connect(self.dang_nhap_tai_khoan)
        # Xoá nội dung ở màn hình đăng nhập
        self.uic.btn_dang_nhap_clear.clicked.connect(self.xoa_content_dang_nhap)
        # Nút chuyển màn hình từ màn hình đăng nhập sang màn hình quên mật khẩu
        self.uic.btn_dang_nhap_quen_mk.clicked.connect(self.display_quen_mat_khau)



        #MÀN HÌNH GIÁM THỊ (ĐÃ ĐĂNG NHẬP)
        #Khai báo một số nút ở màn hình giám thị
        # Nút từ màn hình giám thị trở về màn hình đăng nhập
        self.uic.btn_giam_thi_menu_return.clicked.connect(self.display_dang_nhap_tk)
        # Nút thoát ở màn hình giám thị
        self.uic.btn_giam_thi_menu_close.clicked.connect(self.close)
        # Nút từ màn hình giám thị sang màn hình quét điện thoại
        # self.uic.btn_giam_thi_quet_dien_thoai.clicked.connect(self.display_quet_dien_thoai)
        # Nút từ màn hình giám thị qua màn hình quản lí học sinh
        self.uic.btn_giam_thi_qlhs.clicked.connect(self.display_qlhs)
        # Nút từ màn hình giám thị sang màn hình thông tin tài khoản
        #self.uic.btn_giam_thi_tttk.clicked.connect(self.thong_tin_tai_khoan)

        #MÀN HÌNH QUẢN LÍ HỌC SINH
        #Khai báo một số nút ở màn hình quản lí học sinh
        # Mở file học sinh vi phạm
        self.uic.btn_qlhs_hoc_sinh_vp.clicked.connect(self.open_data_base_hsvp)
        # Mở kênh thông báo
        self.uic.btn_qlhs_telegram.clicked.connect(self.open_thong_bao)
        # Mở cơ sở dữ liệu mã QR
        self.uic.btn_qlhs_ma_qr.clicked.connect(self.open_data_base_qr)
        # Nút cơ sở dữ liệu google sheet
        self.uic.btn_qlhs_du_lieu_hs.clicked.connect(self.co_so_du_lieu)
        # Nút từ màn hình quản lí học sinh trở về màn hình giám thị
        self.uic.btn_qlhs_return.clicked.connect(self.display_man_hinh_giam_thi)
        # Nút thoát trong màn hình quản lí học sinh
        self.uic.btn_qlhs_close.clicked.connect(self.close)




        #MÀN HÌNH QUÉT ĐIỆN THOẠI
        #Khai báo một số nút ở màn hình quét điện thoại
        # Nút từ màn hình quét điện thoại trở về màn hình giám thị
        self.uic.btn_quet_dien_thoai_return.clicked.connect(self.display_man_hinh_giam_thi)
        # Nút thoát ở màn hình quét điện thoại
        self.uic.btn_quet_dien_thoai_close.clicked.connect(self.close)
        # Nút quét các thiết bị
        self.uic.btn_quet_dien_thoai.clicked.connect(self.scan_phone)
        #Nút sao chép địa chỉ IP
        self.uic.btn_xoa_man_hinh.clicked.connect(self.clear_ip)

        #MÀN HÌNH GIÁM SÁT RỘNG
        #Khai báo một số nút ở màn hình giám sát rộng
        # Nút từ màn hình giám sát rộng trở về màn hình học sinh
        self.uic.btn_detect_far_return.clicked.connect(self.display_giam_sat_rong_return)
        # Nút thoát trong màn hình giám sát rộng
        self.uic.btn_detect_far_close.clicked.connect(self.close)
        #Nút mở camera
        self.uic.btn_detect_far_open_camera.clicked.connect(self.open_camera_detect_far)
        #Nút dừng camera của dám sát rộng
        self.uic.btn_detect_far_ready.clicked.connect(self.stop_camera_detect_far_test)
        #Nút bắt đầu giám sát
        self.uic.btn_detect_far_start_detect_new.clicked.connect(self.start_detect_far_new)
        #Nút dừng giám sát rộng
        self.uic.btn_detect_far_stop.clicked.connect(self.stop_detect_far)
        #Nút xoá thông tin
        self.uic.btn_detect_far_clear.clicked.connect(self.clear_screen_detect_far)



        #MÀN HÌNH QUÊN MẬT KHẨU
        #Khai báo một số nút ở màn hình quên mật khẩu
        # Nút từ màn hình quên mật khẩu trở về màn hình đăng nhập
        self.uic.btn_quen_mk_return.clicked.connect(self.display_dang_nhap_tk)
        # Nút thoát trong màn hình quên mật khẩu
        self.uic.btn_quen_mk_close.clicked.connect(self.close)
        # Nút lấy lại mật khẩu
        self.uic.btn_quen_mk_start.clicked.connect(self.lay_lai_mat_khau)
        # Xoá nội dung trong màn hình lấy lại mật khẩu
        self.uic.btn_quen_mk_clear.clicked.connect(self.xoa_content_quen_mk)
        # Nút từ màn hình quên mật khẩu về màn hình đăng nhập
        self.uic.btn_quen_mk_return.clicked.connect(self.display_dang_nhap_tk)
        # Nút thoát màn hình quên mật khẩu
        self.uic.btn_quen_mk_close.clicked.connect(self.close)


        #MÀN HÌNH THÔNG TIN TÀI KHOẢN
        #Khai báo màn hình thông tin tài khoản
        # Nút từ màn hình thông tin tài khoản về màn hình giám thị
        #self.uic.btn_thong_tin_tk_return.clicked.connect(self.display_man_hinh_giam_thi)
        # Nút thoát ở màn hình thông tin tài khoản
        #self.uic.btn_thong_tin_tk_close.clicked.connect(self.close)

        #MÀN HÌNH BOT EMAIL
        #Khai báo một số nút ở màn hình bot email
        #Nút từ màn hình bot email trở về màn hình giám sát
        self.uic.btn_student_return.clicked.connect(self.qt_display_detec)
        #Nút thoát ở màn hình bot email
        self.uic.btn_student_close.clicked.connect(self.close)
        #Nút ghi dữ liệu ở màn hình bot email
        self.uic.btn_student_bot.clicked.connect(self.ghi_bot_mail)
        #MÀN HÌNH BOT QR
        #Khai báo một số nút ở màn hình bot qr
        #Nút trở về ở màn hình tạo mã QR
        self.uic.btn_bot_qr_return.clicked.connect(self.qt_display_make_data_qr)
        #Nút thoát ở màn hình BOT QR TXT
        self.uic.btn_qr_bot_close.clicked.connect(self.close)
        #Nút ghi nhận dữ liệu
        self.uic.btn_qr_bot.clicked.connect(self.ghi_nhan_data_token_qr)


        #MÀN HÌNH THÔNG BÁO
        #Khai báo một số nút ở màn hình thông báo
        #Học sinh vi phạm
        self.uic.btn_lvt_hs_vp.clicked.connect(self.le_van_tam_hsvp)
        #Mã QR học sinh
        self.uic.btn_lvt_qr.clicked.connect(self.le_van_tam_maqrhs)
        #Mã QR điện thoại
        self.uic.btn_lvt_qr_group.clicked.connect(self.le_van_tam_qrdt)
        #Nút thoát ở màn hình thông báo
        self.uic.btn_thong_bao_close.clicked.connect(self.close)
        #Hàm trở về màn hình giám sát học sinh
        self.uic.btn_thong_bao_return.clicked.connect(self.display_qlhs)
        #Nút trở về màn hình
        self.uic.btn_screen_lvt_rt.clicked.connect(self.open_thong_bao)
        #Nút thoát
        self.uic.btn_screen_lvt_close.clicked.connect(self.close)


        #Học sinh vi phạm
        self.uic.btn_mtt_hs_vp.clicked.connect(self.mai_thanh_the_hsvp)
        #Mã QR học sinh
        self.uic.btn_mtt_qr.clicked.connect(self.mai_thanh_the_maqrhs)
        #Mã QR điện thoại
        self.uic.btn_mtt_qr_group.clicked.connect(self.mai_thanh_the_qrdt)
        #Trở về màn hình
        self.uic.btn_screen_mtt_rt.clicked.connect(self.open_thong_bao)
        #Nt thoát
        self.uic.btn_screen_mtt_close.clicked.connect(self.close)



        #Học sinh vi phạm
        self.uic.btn_tvb_hs_vp.clicked.connect(self.tran_van_bay_hsvp)
        #Mã QR học sinh
        self.uic.btn_tvb_qr.clicked.connect(self.tran_van_bay_maqrhs)
        #Mã QR điện thoại
        self.uic.btn_tvb_qr_group.clicked.connect(self.tran_van_bay_qrdt)
        #Trở về màn hình
        self.uic.btn_screen_tvb_rt.clicked.connect(self.open_thong_bao)
        #Thoát
        self.uic.btn_screen_tvb_close.clicked.connect(self.close)


        #Học sinh vi phạm
        self.uic.btn_vl_hs_vp.clicked.connect(self.vinh_loi_hsvp)
        #Mã QR học sinh
        self.uic.btn_vl_qr.clicked.connect(self.vinh_loi_maqrhs)
        #Mã QR điện thoại
        self.uic.btn_vl_qr_group.clicked.connect(self.vinh_loi_qrdt)
        #Nút về màn hình thông báo
        self.uic.btn_screen_vl_rt.clicked.connect(self.open_thong_bao)
        #Nút thoát
        self.uic.btn_screen_vl_close.clicked.connect(self.close)




        #MÀN HÌNH TIỆN ÍCH
        # #Trở về màn hình học sinh
        # self.uic.btn_tien_ich_rt.clicked.connect(self.display_student)
        # #Thoát ở màn hình tiện ích
        # self.uic.btn_tien_ich_close.clicked.connect(self.close)
        # #Mở màn bảng tuần hoàn hoá học
        # self.uic.btn_tien_ich_bth.clicked.connect(self.open_bang_tuan_hoa)
        # #Mở máy tính casio
        # self.uic.btn_tien_ich_casio.clicked.connect(self.open_casio)
        # #Mở phân biệt hidr
        # self.uic.btn_tien_ich_hc.clicked.connect(self.open_hidro_cacbon)


        #MÀN HÌNH ĐIỂM DANH MỚI
        #Nút trở về ở màn hình điểm danh mới
        self.uic.btn_attendance_far_return.clicked.connect(self.return_display_attendance)
        #Nút thoát ở màn hình điểm danh
        self.uic.btn_attendance_far_close.clicked.connect(self.close)
        #Nút bắt đầu điểm danh
        self.uic.btn_attendance_far_start_attendance.clicked.connect(self.start_attendace_far)
        #Nút dừng điểm danh
        self.uic.btn_attendance_far_stop.clicked.connect(self.attendance_far_stop)
        #Nút chuyển sang màn hình tạo mã qr
        self.uic.btn_data_create_qr.clicked.connect(self.qt_display_make_data_qr)
        #Nút chọn chế độ điểm danh
        # self.uic.btn_mode_attendance.clicked.connect(self.mode_attendance)




        #MÀN HÌNH TẠO DỮ LIỆU THỜI GIAN
        #Nút quay trở về menu lựa chọn điểm danh
        self.uic.btn_setup_time_return.clicked.connect(self.return_display_time)
        #Nút thoát ở màn hình tạo dữ liệu
        self.uic.btn_setup_time_close.clicked.connect(self.close)
        #Nút buổi
        self.uic.btn_buoi.clicked.connect(self.mode_time_set)
        #Nút xác nhận
        self.uic.btn_xac_nhan_time.clicked.connect(self.creat_file_time)
        #Nút xoá nội dung
        self.uic.btn_clear.clicked.connect(self.clear_content_input)
        #Nút mở thư mục
        self.uic.btn_folder_time.clicked.connect(self.open_folder_time)


        #MÀN HÌNH LỰA CHỌN MÔN HỌC
        #Môn toán
        self.uic.btn_toan.clicked.connect(self.sl_toan)
        #Môn vật lí
        self.uic.btn_vat_li.clicked.connect(self.sl_vat_li)
        #Môn hoá học
        self.uic.btn_hoa_hoc.clicked.connect(self.sl_hoa_hoc)
        #Môn sinh học
        self.uic.btn_sinh_hoc.clicked.connect(self.sl_sinh_hoc)
        #Môn tiếng anh
        self.uic.btn_tieng_anh.clicked.connect(self.sl_tieng_anh)
        #Môn ngữ văn
        self.uic.btn_ngu_van.clicked.connect(self.sl_ngu_van)
        #Môn địa lí
        self.uic.btn_dia_li.clicked.connect(self.sl_dia_li)
        #Môn GDCD
        self.uic.btn_GDCD.clicked.connect(self.sl_GDCD)
        #Môn lịch sử
        self.uic.btn_lich_su.clicked.connect(self.sl_lich_su)
        #Môn mĩ thuật
        self.uic.btn_mi_thuat.clicked.connect(self.sl_mi_thuat)
        #Môn âm nhạc
        self.uic.btn_am_nhac.clicked.connect(self.sl_am_nhac)
        #Môn gdqp
        self.uic.btn_gdqp.clicked.connect(self.sl_gdqp)
        #Môn thể dục
        self.uic.btn_td.clicked.connect(self.sl_td)
        #Môn tin học
        self.uic.btn_tin_hoc.clicked.connect(self.sl_tin_hoc)
        #Môn tin học nghề
        self.uic.btn_tin_hoc_nghe.clicked.connect(self.sl_tin_hoc_nghe)

        #MÀN HÌNH GIÁM SÁT RỘNG
        #Nút trở về màn hình giám sát rộng
        self.uic.btn_giam_sat_rong_return.clicked.connect(self.display_giam_sat_rong_return)
        #Nút thoát
        self.uic.btn_giam_sat_rong_close.clicked.connect(self.close)
        #Nút chọn nguồn dẫn link
        self.uic.btn_detect_far_link.clicked.connect(self.option_link)
        #Nút bắt đầu giám sát rộng
        self.uic.btn_detect_far_start.clicked.connect(self.detect_far_start)
        #Nút dừng giám sát diện rộng
        self.uic.btn_giam_sat_rong_stop.clicked.connect(self.detect_far_stop)



        #MÀN HÌNH ĐIỂM DANH BẰNG QR
        self.uic.btn_menu_attendance_qr.clicked.connect(self.display_qr_code)
        #Nút trở về màn hình điểm danh
        # self.uic.btn_attendance_qr_detect_return.clicked.connect(self.display_hoc_sinh)
        #Nút thoát
        self.uic.btn_attendance_qr_detect_close.clicked.connect(self.close)


        #Nút chọn nguồn file
        # self.uic.btn_source_file.clicked.connect(self.chose_file_source)
        #Nút nộp bài
        #self.uic.btn_type_test_40_submit.clicked.connect(self.submit_test)

        #Mở thư mục kiểm tra bài làm của học sinh
        #self.uic.btn_xem_ket_qua.clicked.connect(self.open_folder_thi_sinh)

        #Nút mở xem kết quả bài làm
        #self.uic.btn_xem_ket_qua_bai_lam.clicked.connect(self.xem_ket_qua_bai_lam)

        #Nút trở về của màn hình
        self.uic.btn_xem_ket_qua_return.clicked.connect(self.display_thi_sinh_thi)


        #Nút vào màn hình xem lại bài
        # self.uic.btn_tra_cuu_diem.clicked.connect(self.display_tra_cuu_diem)

        # #Options kiểm tra
        # #Danh sách loại
        # type_test = ["Kiểm tra thường xuyên lần 1","Kiểm tra thường xuyên lần 2","Kiểm tra thường xuyên lần 3","Kiểm tra thường xuyên lần 4","Kiểm tra thường xuyên lần 5","Kiểm tra thường xuyên lần 6","Kiểm tra thường xuyên lần 7","Kiểm tra thường xuyên lần 8","Kiểm tra thường xuyên lần 9","Kiểm tra giữa kì I","Kiểm tra cuối kì I","Kiểm tra giữa kì II","Kiểm tra cuối kì II"]
        # #Tạo đối tượng
        # completer_type = QCompleter(type_test,self.uic.btn_name_type_kt)
        # # Thiết lập QCompleter cho QLineEdit
        # self.uic.btn_name_type_kt.setCompleter(completer_type)
        # #Danh sách tên trường
        # #Danh sách loại
        # type_schools = ['THCS Nguyễn Tri Phương',"THCS Nguyễn Tri Phương","THCS Nguyễn Tri Phương","THCS Nguyễn Tri Phương","THCS Nguyễn Tri Phương","THCS Nguyễn Tri Phương"]
        # #Tạo đối tượng
        # completer_type = QCompleter(type_schools,self.uic.btn_name_school)
        # # Thiết lập QCompleter cho QLineEdit
        # self.uic.btn_name_school.setCompleter(completer_type)
        #
        # #Tạo môn
        # type_mon = ["Môn Toán","Môn Ngữ Văn","Môn Ngoại ngữ","Môn Tin học","Môn Sinh học","Môn Địa lí","Môn Hoá học","Môn Lịch sử","Môn GDCD","Môn GDQP","Môn Âm nhạc","Môn Mĩ thuật","Môn Vật lí"]
        # completer_type = QCompleter(type_mon,self.uic.btn_name_subject)
        # # Thiết lập QCompleter cho QLineEdit
        # self.uic.btn_name_subject.setCompleter(completer_type)
        #
        #
        # #Tạo bài kiểm tra
        # #self.uic.btn_tao_ma_bai_kiem_tra.clicked.connect(self.create_test)
        # #Mở thư mục lấy đề
        # self.uic.btn_open_de.clicked.connect(self.open_de_hs_new)
        # #Mở thư mục đáp án
        # self.uic.btn_nhap_dap_an.clicked.connect(self.open_dap_an)
        #
        # #PHIẾU KIỂM TRA CỦA THÍ SINH
        # #Danh sách loại
        # type_test_new = ["Kiểm tra thường xuyên lần 1","Kiểm tra thường xuyên lần 2","Kiểm tra thường xuyên lần 3","Kiểm tra thường xuyên lần 4","Kiểm tra thường xuyên lần 5","Kiểm tra thường xuyên lần 6","Kiểm tra thường xuyên lần 7","Kiểm tra thường xuyên lần 8","Kiểm tra thường xuyên lần 9","Kiểm tra giữa kì I","Kiểm tra cuối kì I","Kiểm tra giữa kì II","Kiểm tra cuối kì II"]
        # #Tạo đối tượng
        # completer_type = QCompleter(type_test_new,self.uic.btn_name_type_test)
        # # Thiết lập QCompleter cho QLineEdit
        # self.uic.btn_name_type_test.setCompleter(completer_type)


        #Danh sách tên trường
        #Danh sách loại
        # type_schools_new = ['THCS Nguyễn Tri Phương',"THCS Nguyễn Tri Phương","THCS Nguyễn Tri Phương","THCS Nguyễn Tri Phương","THCS Nguyễn Tri Phương","THCS Nguyễn Tri Phương"]
        #Tạo đối tượng
        # completer_type_new = QCompleter(type_schools,self.uic.btn_ten_truong)
        # # Thiết lập QCompleter cho QLineEdit
        # self.uic.btn_ten_truong.setCompleter(completer_type_new)

        #Nút mở đề
        #self.uic.btn_type_test_40_open.clicked.connect(self.open_de_new)


        #Tạo môn
        type_mon_new = ["Môn Toán","Môn Ngữ Văn","Môn Ngoại ngữ","Môn Tin học","Môn Sinh học","Môn Địa lí","Môn Hoá học","Môn Lịch sử","Môn GDCD","Môn GDQP","Môn Âm nhạc","Môn Mĩ thuật","Môn Vật lí"]
        completer_type = QCompleter(type_mon_new,self.uic.btn_name_sub_test)
        # Thiết lập QCompleter cho QLineEdit
        self.uic.btn_name_sub_test.setCompleter(completer_type)




        #Nút qua màn hình cập nhật dữ liệu
        self.uic.btn_attendance_update_data_2.clicked.connect(self.display_update_data_new)


    def display_update_data_new(self):
        self.uic.main_widget.setCurrentWidget(self.uic.diplay_attendance_update_data_face)

    #Màn hình tra cứu điểm
    def display_tra_cuu_diem(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_xem_lai_bai)

    #Màn hình thí sinh thi
    def display_thi_sinh_thi(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_type_test)

    #def xem_ket_qua_bai_lam(self):
        #Lấy mã bài làm
    #     ma_bai_lam = self.uic.input_ma_bai_lam.text()
    #     so_bao_danh = self.uic.input_so_bao_danh.text()
    #     mang = ma_bai_lam.split(".")
    #     ma_de = mang[0]
    #     ten_truong = mang[1]
    #     ten_lop = mang[2]
    #     ten_bai = mang[3]
    #     ten_mon = mang[4]
    #     so_cau = mang[5]
    #
    #     #Kiểm tra xem số báo danh đó có không
    #     import openpyxl as op
    #     wb = op.load_workbook(f"Thong_tin_thi_sinh/{ten_truong}_{ten_mon}_{ten_bai}.xlsx")
    #     Sheet1 = wb["Sheet"]
    #     wb.close()
    #     #Xác định cột
    #     column_test = "B"
    #     #Giá trị của cột
    #     column = Sheet1[column_test]
    #     #Mảng chứa dữ liệu trong cột
    #     column_data = []
    #     #Duyệt qua từng cột
    #     for cell in column:
    #         column_data.append(cell.value)
    #
    #
    #     print("Dữ liệu trong mảng số báo danh là",column_data)
    #     if so_bao_danh in column_data:
    #         print("Mảng là",mang)
    #         print(f"Ket_qua_thi_sinh/{mang[1]}_{so_bao_danh}_{mang[2]}_{mang[3]}_{mang[4]}.txt")
    #         f = open(f"Ket_qua_thi_sinh/{mang[1]}_{so_bao_danh}_{mang[2]}_{mang[3]}_{mang[4]}.txt", mode = "r",encoding="utf-8-sig")
    #         thong_tin = f.read()
    #         print("Thông tin là",thong_tin)
    #         f.close()
    #         #Đọc thời gian
    #         ma_de = mang[0]
    #         ten_truong = mang[1]
    #
    #         ten_lop = mang[2]
    #         ten_bai = mang[3]
    #         ten_mon = mang[4]
    #         so_cau = mang[5]
    #
    #         f = open(f"Thoi_gian_test/Time_{ten_truong}_{ma_de}_{ten_lop}_{ten_bai}_{ten_mon}_{so_cau}.txt",mode = "r",encoding="utf-8-sig")
    #         thoi_gian_mang = f.read().split(",")
    #         f.close()
    #         print("Mảng thời gian nộp đề là",thoi_gian_mang)
    #         # gio_bd = int(thoi_gian_mang[0])
    #         # phut_bd = int(thoi_gian_mang[1])
    #         gio_kt = int(thoi_gian_mang[2])
    #         phut_kt = int(thoi_gian_mang[3])
    #         thoi_gian_hien_tai = datetime.datetime.now()
    #         gio_hien_tai = thoi_gian_hien_tai.hour
    #         phut_hien_tai = thoi_gian_hien_tai.minute
    #         if gio_hien_tai == gio_kt and phut_hien_tai < phut_kt:
    #             QMessageBox.information(self,"Thông báo",f"Chưa đến thời gian xem kết quả ! \nKết quả được mở vào lúc {gio_kt}:{phut_kt}")
    #         elif gio_hien_tai < gio_kt:
    #             QMessageBox.information(self,"Thông báo",f"Chưa đến thời gian xem kết quả ! \nKết quả được mở vào lúc {gio_kt}:{phut_kt}")
    #         else:
    #             self.uic.show_ket_qua_lam_bai.setText(f"{thong_tin}")
    #     else:
    #         QMessageBox.information(self,"Thông báo","Không tìm thấy số báo danh vừa nhập. Vui lòng kiểm tra lại số báo danh!")
    #
    #
    #
    # #Mở thư mục làm bài của thí sinh
    # def open_folder_thi_sinh(self):
    #     import webbrowser
    #     path = "Thong_tin_thi_sinh"
    #     webbrowser.open(path)

    #Nộp bài
    #def submit_test(self):
#         ten_bai = self.uic.btn_name_type_test.text()
#         ten_truong = self.uic.btn_ten_truong.text()
#         ten_lop = self.uic.btn_name_class_test.text()
#         ten_mon = self.uic.btn_name_sub_test.text()
#         so_cau = int(self.uic.btn_so_cau_lam.text())
#         print("Số câu là",so_cau)
#         ten_bai = rut_gon_ten_bai(ten_bai)
#         ten_truong = rut_gon_ten_truong(ten_truong)
#         ten_mon = rut_gon_ten_mon(ten_mon)
#         ma_de = self.uic.btn_code.text()
#         sbd = self.uic.btn_sbd_test.text()
#         ten_hoc_sinh = self.uic.btn_name_student_test.text()
#
#         #Đọc tệp đáp án
#         import openpyxl
#         # Mở tệp Excel
#         wb = openpyxl.load_workbook(f'Dap_an/{ma_de}_{ten_truong}_{ten_lop}_{ten_bai}_{ten_mon}_{so_cau}.xlsx')
#         # Chọn sheet
#         sheet = wb['Sheet']
#         # Lấy giá trị từ một cột cụ thể
#         mang_dap_an = [cell.value for cell in sheet['A']]  # 'A' là tên cột cần đọc
#         # In ra dữ liệu trong cột
#         print(mang_dap_an)
#
#         #Lấy giá trị bài làm
#         bl_1 = self.uic.input_120c_01.text()
#         bl_2 = self.uic.input_120c_02.text()
#         bl_3 = self.uic.input_120c_03.text()
#         bl_4 = self.uic.input_120c_04.text()
#         bl_5 = self.uic.input_120c_05.text()
#         bl_6 = self.uic.input_120c_06.text()
#         bl_7 = self.uic.input_120c_07.text()
#         bl_8 = self.uic.input_120c_08.text()
#         bl_9 = self.uic.input_120c_09.text()
#         bl_10 = self.uic.input_120c_10.text()
#         bl_11 = self.uic.input_120c_11.text()
#         bl_12 = self.uic.input_120c_12.text()
#         bl_13 = self.uic.input_120c_13.text()
#         bl_14 = self.uic.input_120c_14.text()
#         bl_15 = self.uic.input_120c_15.text()
#         bl_16 = self.uic.input_120c_16.text()
#         bl_17 = self.uic.input_120c_17.text()
#         bl_18 = self.uic.input_120c_18.text()
#         bl_19 = self.uic.input_120c_19.text()
#         bl_20 = self.uic.input_120c_20.text()
#         bl_21 = self.uic.input_120c_21.text()
#         bl_22 = self.uic.input_120c_22.text()
#         bl_23 = self.uic.input_120c_23.text()
#         bl_24 = self.uic.input_120c_24.text()
#         bl_25 = self.uic.input_120c_25.text()
#         bl_26 = self.uic.input_120c_26.text()
#         bl_27 = self.uic.input_120c_27.text()
#         bl_28 = self.uic.input_120c_28.text()
#         bl_29 = self.uic.input_120c_29.text()
#         bl_30 = self.uic.input_120c_30.text()
#         bl_31 = self.uic.input_120c_31.text()
#         bl_32 = self.uic.input_120c_32.text()
#         bl_33 = self.uic.input_120c_33.text()
#         bl_34 = self.uic.input_120c_34.text()
#         bl_35 = self.uic.input_120c_35.text()
#         bl_36 = self.uic.input_120c_36.text()
#         bl_37 = self.uic.input_120c_37.text()
#         bl_38 = self.uic.input_120c_38.text()
#         bl_39 = self.uic.input_120c_39.text()
#         bl_40 = self.uic.input_120c_40.text()
#         bl_41 = self.uic.input_120c_41.text()
#         bl_42 = self.uic.input_120c_42.text()
#         bl_43 = self.uic.input_120c_43.text()
#         bl_44 = self.uic.input_120c_44.text()
#         bl_45 = self.uic.input_120c_45.text()
#         bl_46 = self.uic.input_120c_46.text()
#         bl_47 = self.uic.input_120c_47.text()
#         bl_48 = self.uic.input_120c_48.text()
#         bl_49 = self.uic.input_120c_49.text()
#         bl_50 = self.uic.input_120c_50.text()
#         bl_51 = self.uic.input_120c_51.text()
#         bl_52 = self.uic.input_120c_52.text()
#         bl_53 = self.uic.input_120c_53.text()
#         bl_54 = self.uic.input_120c_54.text()
#         bl_55 = self.uic.input_120c_55.text()
#         bl_56 = self.uic.input_120c_56.text()
#         bl_57 = self.uic.input_120c_57.text()
#         bl_58 = self.uic.input_120c_58.text()
#         bl_59 = self.uic.input_120c_59.text()
#         bl_60 = self.uic.input_120c_60.text()
#         bl_61 = self.uic.input_120c_61.text()
#         bl_62 = self.uic.input_120c_62.text()
#         bl_63 = self.uic.input_120c_63.text()
#         bl_64 = self.uic.input_120c_64.text()
#         bl_65 = self.uic.input_120c_65.text()
#         bl_66 = self.uic.input_120c_66.text()
#         bl_67 = self.uic.input_120c_67.text()
#         bl_68 = self.uic.input_120c_68.text()
#         bl_69 = self.uic.input_120c_69.text()
#         bl_70 = self.uic.input_120c_70.text()
#         bl_71 = self.uic.input_120c_71.text()
#         bl_72 = self.uic.input_120c_72.text()
#         bl_73 = self.uic.input_120c_73.text()
#         bl_74 = self.uic.input_120c_74.text()
#         bl_75 = self.uic.input_120c_75.text()
#         bl_76 = self.uic.input_120c_76.text()
#         bl_77 = self.uic.input_120c_77.text()
#         bl_78 = self.uic.input_120c_78.text()
#         bl_79 = self.uic.input_120c_79.text()
#         bl_80 = self.uic.input_120c_80.text()
#         bl_81 = self.uic.input_120c_81.text()
#         bl_82 = self.uic.input_120c_82.text()
#         bl_83 = self.uic.input_120c_83.text()
#         bl_84 = self.uic.input_120c_84.text()
#         bl_85 = self.uic.input_120c_85.text()
#         bl_86 = self.uic.input_120c_86.text()
#         bl_87 = self.uic.input_120c_87.text()
#         bl_88 = self.uic.input_120c_88.text()
#         bl_89 = self.uic.input_120c_89.text()
#         bl_90 = self.uic.input_120c_90.text()
#         bl_91 = self.uic.input_120c_91.text()
#         bl_92 = self.uic.input_120c_92.text()
#         bl_93 = self.uic.input_120c_93.text()
#         bl_94 = self.uic.input_120c_94.text()
#         bl_95 = self.uic.input_120c_95.text()
#         bl_96 = self.uic.input_120c_96.text()
#         bl_97 = self.uic.input_120c_97.text()
#         bl_98 = self.uic.input_120c_98.text()
#         bl_99 = self.uic.input_120c_99.text()
#         bl_100 = self.uic.input_120c_100.text()
#         bl_101 = self.uic.input_120c_101.text()
#         bl_102 = self.uic.input_120c_102.text()
#         bl_103 = self.uic.input_120c_103.text()
#         bl_104 = self.uic.input_120c_104.text()
#         bl_105 = self.uic.input_120c_105.text()
#         bl_106 = self.uic.input_120c_106.text()
#         bl_107 = self.uic.input_120c_107.text()
#         bl_108 = self.uic.input_120c_108.text()
#         bl_109 = self.uic.input_120c_109.text()
#         bl_110 = self.uic.input_120c_110.text()
#         bl_111 = self.uic.input_120c_111.text()
#         bl_112 = self.uic.input_120c_112.text()
#         bl_113 = self.uic.input_120c_113.text()
#         bl_114 = self.uic.input_120c_114.text()
#         bl_115 = self.uic.input_120c_115.text()
#         bl_116 = self.uic.input_120c_116.text()
#         bl_117 = self.uic.input_120c_117.text()
#         bl_118 = self.uic.input_120c_118.text()
#         bl_119 = self.uic.input_120c_119.text()
#         bl_120 = self.uic.input_120c_120.text()
#         mang_bai_lam = [bl_1,bl_2,bl_3,bl_4,bl_5,bl_6,bl_7,bl_8,bl_9,bl_10,bl_11,bl_12,bl_13,bl_14,bl_15,bl_16,bl_17, bl_18 ,bl_19,bl_20,bl_21,bl_22,bl_23,bl_24,bl_25,bl_26,bl_27,bl_28,bl_29,bl_30,bl_31,bl_32,bl_33,bl_34,bl_35,bl_36,bl_37,bl_38,bl_39,bl_40,bl_41,bl_42,bl_43,bl_44,bl_45,bl_46,bl_47,bl_48,bl_49,bl_50,bl_51,bl_52,bl_53,bl_54,bl_55,bl_56,bl_57,bl_58,bl_59,bl_60,bl_61,bl_62,bl_63,bl_64,bl_65,bl_66,bl_67,bl_68,bl_69,bl_70,bl_71,bl_72,bl_73,bl_74,bl_75,bl_76,bl_77,bl_78,bl_79,bl_80,bl_81,bl_82,bl_83,bl_84,bl_85,bl_86,bl_87,bl_88,bl_89,bl_90,bl_91,bl_92,bl_93,bl_94,bl_95,bl_96,bl_97,bl_98,bl_99,bl_100,bl_101,bl_102,bl_103,bl_104,bl_105,bl_106,bl_107,bl_108,bl_109,bl_110,bl_111,bl_112,bl_113,bl_114,bl_115,bl_116,bl_117,bl_118,bl_119,bl_120]
#         print("Mảng bài làm là",mang_bai_lam)
#         so_cau_dung = 0
#         mang_cau_sai = []
#         for i in range(so_cau):
#             if mang_bai_lam[i] == mang_dap_an[i]:
#                 so_cau_dung += 1
#
#             else:
#                 kq = i + 1
#                 mang_cau_sai.append(kq)
#         print("Số câu đúng là",so_cau_dung)
#         print("Số câu sai là",len(mang_cau_sai))
#         print("Câu sai là")
#         for k in range(len(mang_cau_sai)):
#             print(f"Câu {mang_cau_sai[k]}")
#         #Ghi đáp án vào file excel
#         import openpyxl
#         # Tạo một workbook mới
#         workbook = openpyxl.Workbook()
#         # Chọn sheet đầu tiên trong workbook
#         sheet = workbook.active
#         mang_bai_test = []
#         #Xử lí đáp án
#         for i in range(int(so_cau)):
#             mang_bai_test.append(mang_dap_an[i])
#         print("Mảng bài test là",mang_bai_test)
#         # Ghi số từ 1 đến 120 theo hàng dọc
#         print("Tới bước vòng lặp")
#         print(type(int(so_cau)),"-",int(so_cau))
#         for j in range(int(so_cau)):
#             cell = sheet.cell(row=j+1, column=1)
#             cell.value = mang_bai_test[j]
#         # Lưu workbook vào một file Excel
#         workbook.save(f'Bai_lam_thi_sinh/{ten_truong}_{sbd}_{ten_bai}_{ten_mon}.xlsx')
#         print("Đã lưu file excel")
#
#         ten_truong_new = self.uic.btn_ten_truong.text()
#
#         so_cau_dung_new = f"{so_cau_dung}/{so_cau}"
#         ten_bai_new = self.uic.btn_name_type_test.text()
#         ten_mon_new = self.uic.btn_name_sub_test.text()
#         #Tạo một workbook
#
#         #Ghi nội dung để thí sinh tra cứu
#         f = open(f"Ket_qua_thi_sinh/{ten_truong}_{sbd}_{ten_lop}_{ten_bai}_{ten_mon}.txt",mode = "w+",encoding="utf-8-sig")
#         f.write(f"Tên thí sinh: {ten_hoc_sinh}\nSố báo danh: {sbd}\nTên bài kiểm tra: {ten_bai_new}\nTên môn: {ten_mon_new}\nSố câu đúng: {so_cau_dung_new}\n")
#         f.write("Các câu sai là:\n")
#         for i in range(len(mang_cau_sai)):
#             f.write(f"+ Câu {mang_cau_sai[i]}\n")
#         f.close()
#         my_token = "6178672765:AAGj3y6PQwBjF9RDoaWJ2qkjOPuWrKOcH6Q"
#         # my_token = "5464649749:AAHxqNAjrNgzYN2gy-mKgjV6GMyyILiMHEk"
#         id = "-4073345095"
#
#         bot = telegram.Bot(token=my_token)
#         file_path = f"Bai_lam_thi_sinh/{ten_truong}_{sbd}_{ten_bai}_{ten_mon}.xlsx"
#         file = open(file_path, 'rb')
#         bot.send_document(chat_id=id,document = file)
#
#         #Đọc thời gian
#         f = open(f"Thoi_gian_test/Time_{ten_truong}_{ma_de}_{ten_lop}_{ten_bai}_{ten_mon}_{so_cau}.txt",mode = "r",encoding="utf-8-sig")
#         thoi_gian_mang = f.read().split(",")
#         f.close()
#         print("Mảng thời gian nộp đề là",thoi_gian_mang)
#         # gio_bd = int(thoi_gian_mang[0])
#         # phut_bd = int(thoi_gian_mang[1])
#         gio_kt = int(thoi_gian_mang[2])
#         phut_kt = int(thoi_gian_mang[3])
#         thoi_gian_hien_tai = datetime.datetime.now()
#         gio_hien_tai = thoi_gian_hien_tai.hour
#         phut_hien_tai = thoi_gian_hien_tai.minute
#         nhan_xet = ""
#         if gio_hien_tai == gio_kt and phut_hien_tai > phut_kt:
#             QMessageBox.information(self,"Thông báo vi phạm","Bạn đã vượt quá thời gian làm bài ! \nCode: (1)")
#             nhan_xet = "Nộp bài trễ"
#         elif gio_hien_tai > gio_kt:
#             QMessageBox.information(self,"Thông báo vi phạm","Bạn đã vượt quá thời gian làm bài !\nCode: (2)")
#             nhan_xet = "Nộp bài trễ"
#         else:
#             QMessageBox.information(self,"Thông báo","Bạn đã nộp bài thành công !")
#    #     giay_hien_tai = thoi_gian_hien_tai.second
#   #      time = f"{gio_hien_tai}:{phut_hien_tai}:{giay_hien_tai}"
#  #       #Ghi thông tin thí sinh vào file excel
# #        write_data_student_excel(ten_hoc_sinh,sbd,ten_truong_new,ten_lop,so_cau_dung_new,ten_truong,ten_mon,ten_bai,ten_mon_new,time,nhan_xet)
#






















    #Mở thư mục đề cho học sinh
    #def open_de_new(self):
        # print("Nút mở đề")
        # ten_bai = self.uic.btn_name_type_test.text()
        # ten_truong = self.uic.btn_ten_truong.text()
        # ten_lop = self.uic.btn_name_class_test.text()
        # ten_mon = self.uic.btn_name_sub_test.text()
        # so_cau = int(self.uic.btn_so_cau_lam.text())
        # print("Rút gọn tên bài")
        # ten_bai = rut_gon_ten_bai(ten_bai)
        # print("Rút gọn tên trường")
        # ten_truong = rut_gon_ten_truong(ten_truong)
        # print("Rút gọn tên môn")
        # ten_mon = rut_gon_ten_mon(ten_mon)
        # ma_de = self.uic.btn_code.text()
        # f = open(f"Thoi_gian_test/Time_{ten_truong}_{ma_de}_{ten_lop}_{ten_bai}_{ten_mon}_{so_cau}.txt", mode = "r", encoding="utf-8-sig")
        # tg = f.read()
        # thoi_gian= tg.split(",")
        # print("Thời gian b là",thoi_gian)
        # gio_bd = int(thoi_gian[0])
        # phut_bd = int(thoi_gian[1])
        # gio_kt = int(thoi_gian[2])
        # phut_kt = int(thoi_gian[3])
        # hien_tai = datetime.datetime.now()
        # gio_hien_tai = hien_tai.hour
        # phut_hien_tai = hien_tai.minute
        # print("Giờ hiện tại là ",gio_hien_tai)
        # print("Phút hiện tại là",phut_hien_tai)
        # if gio_hien_tai >= gio_bd and phut_hien_tai >= phut_bd:
        #     import os
        #     file_path = f"DE_HOC_SINH/{ten_truong}_{ma_de}_{ten_bai}_{ten_lop}_{ten_mon}_{so_cau}.pdf"
        #     a = file_path.replace("/","\\")
        #     os.startfile(a)
        # else:
        #     QMessageBox.information(self,"Thông báo",f"Chưa đến thời gian mở đề kiểm tra. Vui lòng thử lại sau !\nĐề được mở vào lúc {gio_bd}:{phut_bd}")










    #Mở thư mục
    def open_dap_an(self):
        import webbrowser
        path = "Dap_an"
        webbrowser.open(path)

    #Mở thư mục đề kiểm tra
    # def open_de_hs_new(self):
    #     import webbrowser
    #     path = "DE_HOC_SINH"
    #     webbrowser.open(path)




    #Tạo bài kiểm tra
    # def create_test(self):
    #     nguon = self.uic.btn_file_de.text()
    #     ten_bai = self.uic.btn_name_type_kt.text()
    #     ten_truong = self.uic.btn_name_school.text()
    #     ten_lop = self.uic.btn_name_class.text()
    #     ma_de = self.uic.btn_code_test.text()
    #     gio_bd = self.uic.btn_ip_time_hour.text()
    #     phut_bd = self.uic.btn_ip_time_minute.text()
    #     gio_kt = self.uic.btn_ip_time_hour_2.text()
    #     phut_kt = self.uic.btn_ip_time_minute_2.text()
    #     ten_mon = self.uic.btn_name_subject.text()
    #     so_cau = self.uic.btn_so_cau.text()
    #     ten_bai = rut_gon_ten_bai(ten_bai)
    #     # print("Tên bài là",ten_bai)
    #     ten_truong = rut_gon_ten_truong(ten_truong)
    #     # print("Tên trường đã qua xử lí là:",ten_truong)
    #     ten_bai = rut_gon_ten_bai(ten_bai)
    #     ten_mon = rut_gon_ten_mon(ten_mon)
    #     # print("Tên môn là",ten_mon)
    #     #Tạo mã bài kiểm tra
    #     ma_bai_kt = f"{ma_de}.{ten_truong}.{ten_lop}.{ten_bai}.{ten_mon}.{so_cau}"
    #     print("Mã bài kiểm tra là",ma_bai_kt)
    #     self.uic.lineEdit.setText(f"{ma_bai_kt}")
    #     f = open(f"Thoi_gian_test/Time_{ten_truong}_{ma_de}_{ten_lop}_{ten_bai}_{ten_mon}_{so_cau}.txt",mode = "w+",encoding="utf-8-sig")
    #     f.write(f"{gio_bd},{phut_bd},{gio_kt},{phut_kt}")
    #     f.close()
    #     #Lấy dữ liệu đáp án
    #     so_cau_trong_dap_an = int(so_cau)
    #     mang_dap_an = []
    #     da_1 = self.uic.ip_01.text()
    #     da_2 = self.uic.ip_02.text()
    #     da_3 = self.uic.ip_03.text()
    #     da_4 = self.uic.ip_04.text()
    #     da_5 = self.uic.ip_05.text()
    #     da_6 = self.uic.ip_06.text()
    #     da_7 = self.uic.ip_07.text()
    #     da_8 = self.uic.ip_08.text()
    #     da_9 = self.uic.ip_09.text()
    #     da_10 = self.uic.ip_10.text()
    #     da_11 = self.uic.ip_11.text()
    #     da_12 = self.uic.ip_12.text()
    #     da_13 = self.uic.ip_13.text()
    #     da_14 = self.uic.ip_14.text()
    #     da_15 = self.uic.ip_15.text()
    #     da_16 = self.uic.ip_16.text()
    #     da_17 = self.uic.ip_17.text()
    #     da_18 = self.uic.ip_18.text()
    #     da_19 = self.uic.ip_19.text()
    #     da_20 = self.uic.ip_20.text()
    #     da_21 = self.uic.ip_21.text()
    #     da_22 = self.uic.ip_22.text()
    #     da_23 = self.uic.ip_23.text()
    #     da_24 = self.uic.ip_24.text()
    #     da_25 = self.uic.ip_25.text()
    #     da_26 = self.uic.ip_26.text()
    #     da_27 = self.uic.ip_27.text()
    #     da_28 = self.uic.ip_28.text()
    #     da_29 = self.uic.ip_29.text()
    #     da_30 = self.uic.ip_30.text()
    #     da_31 = self.uic.ip_31.text()
    #     da_32 = self.uic.ip_32.text()
    #     da_33 = self.uic.ip_33.text()
    #     da_34 = self.uic.ip_34.text()
    #     da_35 = self.uic.ip_35.text()
    #     da_36 = self.uic.ip_36.text()
    #     da_37 = self.uic.ip_37.text()
    #     da_38 = self.uic.ip_38.text()
    #     da_39 = self.uic.ip_39.text()
    #     da_40 = self.uic.ip_40.text()
    #     da_41 = self.uic.ip_41.text()
    #     da_42 = self.uic.ip_42.text()
    #     da_43 = self.uic.ip_43.text()
    #     da_44 = self.uic.ip_44.text()
    #     da_45 = self.uic.ip_45.text()
    #     da_46 = self.uic.ip_46.text()
    #     da_47 = self.uic.ip_47.text()
    #     da_48 = self.uic.ip_48.text()
    #     da_49 = self.uic.ip_49.text()
    #     da_50 = self.uic.ip_50.text()
    #     da_51 = self.uic.ip_51.text()
    #     da_52 = self.uic.ip_52.text()
    #     da_53 = self.uic.ip_53.text()
    #     da_54 = self.uic.ip_54.text()
    #     da_55 = self.uic.ip_55.text()
    #     da_56 = self.uic.ip_56.text()
    #     da_57 = self.uic.ip_57.text()
    #     da_58 = self.uic.ip_58.text()
    #     da_59 = self.uic.ip_59.text()
    #     da_60 = self.uic.ip_60.text()
    #     da_61 = self.uic.ip_61.text()
    #     da_62 = self.uic.ip_62.text()
    #     da_63 = self.uic.ip_63.text()
    #     da_64 = self.uic.ip_64.text()
    #     da_65 = self.uic.ip_65.text()
    #     da_66 = self.uic.ip_66.text()
    #     da_67 = self.uic.ip_67.text()
    #     da_68 = self.uic.ip_68.text()
    #     da_69 = self.uic.ip_69.text()
    #     da_70 = self.uic.ip_70.text()
    #     da_71 = self.uic.ip_71.text()
    #     da_72 = self.uic.ip_72.text()
    #     da_73 = self.uic.ip_73.text()
    #     da_74 = self.uic.ip_74.text()
    #     da_75 = self.uic.ip_75.text()
    #     da_76 = self.uic.ip_76.text()
    #     da_77 = self.uic.ip_77.text()
    #     da_78 = self.uic.ip_78.text()
    #     da_79 = self.uic.ip_79.text()
    #     da_80 = self.uic.ip_80.text()
    #     da_81 = self.uic.ip_81.text()
    #     da_82 = self.uic.ip_82.text()
    #     da_83 = self.uic.ip_83.text()
    #     da_84 = self.uic.ip_84.text()
    #     da_85 = self.uic.ip_85.text()
    #     da_86 = self.uic.ip_86.text()
    #     da_87 = self.uic.ip_87.text()
    #     da_88 = self.uic.ip_88.text()
    #     da_89 = self.uic.ip_89.text()
    #     da_90 = self.uic.ip_90.text()
    #     da_91 = self.uic.ip_91.text()
    #     da_92 = self.uic.ip_92.text()
    #     da_93 = self.uic.ip_93.text()
    #     da_94 = self.uic.ip_94.text()
    #     da_95 = self.uic.ip_95.text()
    #     da_96 = self.uic.ip_96.text()
    #     da_97 = self.uic.ip_97.text()
    #     da_98 = self.uic.ip_98.text()
    #     da_99 = self.uic.ip_99.text()
    #     da_100 = self.uic.ip_100.text()
    #     da_101 = self.uic.ip_101.text()
    #     da_102 = self.uic.ip_102.text()
    #     da_103 = self.uic.ip_103.text()
    #     da_104 = self.uic.ip_104.text()
    #     da_105 = self.uic.ip_105.text()
    #     da_106 = self.uic.ip_106.text()
    #     da_107 = self.uic.ip_107.text()
    #     da_108 = self.uic.ip_108.text()
    #     da_109 = self.uic.ip_109.text()
    #     da_110 = self.uic.ip_110.text()
    #     da_111 = self.uic.ip_111.text()
    #     da_112 = self.uic.ip_112.text()
    #     da_113 = self.uic.ip_113.text()
    #     da_114 = self.uic.ip_114.text()
    #     da_115 = self.uic.ip_115.text()
    #     da_116 = self.uic.ip_116.text()
    #     da_117 = self.uic.ip_117.text()
    #     da_118 = self.uic.ip_118.text()
    #     da_119 = self.uic.ip_119.text()
    #     da_120 = self.uic.ip_120.text()
    #     mang_bien = [da_1,da_2,da_3,da_4,da_5,da_6,da_7,da_8,da_9,da_10,da_11,da_12,da_13,da_14,da_15,da_16,da_17,da_18,da_19,da_20,da_21,da_22,da_23,da_24,da_25,da_26,da_27,da_28,da_29,da_30,da_31,da_32,da_33,da_34,da_35,da_36,da_37,da_38,da_39,da_40,da_41,da_42,da_43,da_44,da_45,da_46,da_47,da_48,da_49,da_50,da_51,da_52,da_53,da_54,da_55,da_56,da_57,da_58,da_59,da_60,da_61,da_62,da_63,da_64,da_65,da_66,da_67,da_68,da_69,da_70,da_71,da_72,da_73,da_74,da_75,da_76,da_77,da_78,da_79,da_80,da_81,da_82,da_83,da_84,da_85,da_86,da_87,da_88,da_89,da_90,da_91,da_92,da_93,da_94,da_95,da_96,da_97,da_98,da_99,da_100,da_101,da_102,da_103,da_104,da_105,da_106,da_107,da_108,da_109,da_110,da_111,da_112,da_113,da_114,da_115,da_116,da_117,da_118,da_119,da_120]
    #     for i in range(so_cau_trong_dap_an):
    #         mang_dap_an.append(mang_bien[i])
    #     print("Mảng đáp án là",mang_dap_an)
    #     print("Tới bước ghi excel")
    #     import openpyxl
    #     # Tạo một workbook mới
    #     workbook = openpyxl.Workbook()
    #     # Chọn sheet đầu tiên trong workbook
    #     sheet = workbook.active
    #     # Ghi số từ 1 đến 120 theo hàng dọc
    #     print("Tới bước vòng lặp")
    #     for i in range(so_cau_trong_dap_an):
    #         cell = sheet.cell(row=i+1, column=1)
    #         print("i là",i)
    #         cell.value = mang_dap_an[i]
    #     # Lưu workbook vào một file Excel
    #     print(f"Tên file là: Dap_an/{ma_de}_{ten_truong}_{ten_lop}_{ten_bai}_{ten_mon}_{so_cau}.xlsx")
    #     workbook.save(f'Dap_an/{ma_de}_{ten_truong}_{ten_lop}_{ten_bai}_{ten_mon}_{so_cau}.xlsx')
    #     #Xử lí file tên
    #     import shutil
    #     # Đường dẫn đến file cần copy
    #     link = self.uic.btn_file_de.text()
    #     src_file = f'{link}'
    #     # Đường dẫn đến thư mục đích
    #     dst_folder = 'DE_HOC_SINH'
    #     # Sử dụng hàm shutil.copy() để copy file
    #     shutil.copy(src_file, dst_folder)
    #     #Đổi tên
    #     mang_ten = link.split("/")
    #     if mang_ten[0] != "":
    #         ten_tep = mang_ten[-1]
    #     else:
    #         ten_tep = mang_ten[0]
    #     mang_duoi = ten_tep.split(".")
    #     duoi = mang_duoi[-1]
    #     print("Tên tệp là",ten_tep)
    #     link_old = f"DE_HOC_SINH\\{ten_tep}"
    #     print("Link cũ là",link_old)
    #     link_new = f"DE_HOC_SINH\\{ten_truong}_{ma_de}_{ten_bai}_{ten_lop}_{ten_mon}_{so_cau}.{duoi}"
    #     print("link_mới là", link_new)
    #     os.rename(link_old, link_new)
    #     #Tạo một workbook
    #     #Ghi đáp án vào file excel
    #     import openpyxl
    #     # Tạo một workbook mới
    #     workbook = openpyxl.Workbook()
    #     #Lưu workbook
    #     workbook.save(f"Thong_tin_thi_sinh/{ten_truong}_{ten_mon}_{ten_bai}.xlsx")















    #Chọn file đề
    #def chose_file_source(self):
        #link_data_input = QFileDialog.getOpenFileName(filter="")
        #self.uic.btn_file_de.setText(link_data_input[0])



    #Màn hình tạo bài kiểm tra và xem kết quả
    #def display_tao_xem(self):
        #self.uic.main_widget.setCurrentWidget(self.uic.display_set_up_test)

    #Màn hình tạo bài kiểm tra
    #def display_creat_test_new(self):
        #self.uic.main_widget.setCurrentWidget(self.uic.display_tao_bai_kiem_tra)



    #Từ màn hình lựa chọn kiểm tra về màn hình giám thị
    def display_giam_thi_new(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_giam_thi_menu)

    #Qua màn hình kieểm tra của giám thị
    def display_chose_giam_thi(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_set_up_test)



    #Xem hướng dẫn làm bài
    # def view_huong_dan(self):
    #     QMessageBox.information(self,"Hướng dẫn sử dụng phiếu trắc nghiệm","+ Thí sinh điền đầy đủ thông tin vào mẫu có sẵn \n+ Thí sinh chỉ nhập 1 đáp án vào mỗi ô tương ứng (A, B, C, D) \n+ Sau khi làm bài xong, kiểm tra thật kĩ thông tin và đáp án, sau đó nhận nộp bài \n+ Không được bỏ trống đáp án")


    #MÀN HÌNH PHIẾU TRẢ LỜI TRẮC NGHIỆM
    def display_lam_bai_kiem_tra(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_phieu_kt)

    #MÀN HÌNH KIỂM TRA KIẾN THỨC
    def display_kiem_tra_kien_thuc(self):
         self.uic.main_widget.setCurrentWidget(self.uic.display_type_test)


    #Hàm thông báo
    def show_thong_bao(self,so):
        if so == 1:
            QMessageBox.information(self, "Nhắc nhở thí sinh", "Thí sinh vui lòng nghiêm túc làm bài (Lần 1)")
        elif so == 2:
            QMessageBox.information(self, "Nhắc nhở th sinh", "Thí sinh vui lòng nghiêm túc làm bài (Lần 2)")
        elif so == 3:
            QMessageBox.information(self, "Thông báo thí sinh", "Hệ thống xác nhận bạn đã vi phạm quy chế thi")
        elif so == 4:
            QMessageBox.information(self, "Nhắc nhở thí sinh", "Thí sinh vui lòng không che Camera (Lần 1)")
        elif so == 5:
            QMessageBox.information(self, "Nhắc nhở thí sinh", "Thí sinh vui lòng không che Camera (Lần 2)")
        elif so == 6:
            QMessageBox.information(self, "Thông báo vi phạm", "AI xác nhận bạn đã vi phạm quy chế thi")
    #Từ màn hình giám sát rộng qua màn hình lựa chọn giám sát
    def display_giam_sat_rong_return(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_giam_sat_menu)


    #Từ màn hình lựa chọn 3 cái điểm danh trở về màn hình lựa chọn
    def display_diem_danh(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_diem_danh_menu)



    #Từ màn hình menu tạo dữ liệu trở về màn hình điểm danh, tạo dữ liệu
    def display_menu_tao_du_lieu_return(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_diem_danh_menu)



    #Từ màn hình điểm danh, tạo dữ liệu sang màn hình menu tạo dữ liệu
    def display_menu_tao_du_lieu_new(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_tao_du_lieu)






    #Từ màn hình điểm danh trở về
    def display_menu_diem_danh_return(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_menu_student)



    #Màn hình lựa chọn chế độ giám sát trở về
    def display_menu_giam_sat_return(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_menu_student)



    #Màn hình lựa chọn chế độ giám sát
    def display_giam_sat_new(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_giam_sat_menu)


    #Tạm dừng camera điểm danh khuôn mặt

    def stop_camera_attendance_face(self):
        print("Nhấn vào nút dừng")
        self.thread[4].stop()


    #Sao chép thông tin

    def clear_ip(self):
        self.uic.tinh_trang_quet.setText("")
        self.uic.show_list_devises.setText("Danh sách các thiết bị quét được là:")
    #Hàm từ màn hình quét điện thoại trở về màn hình giám thị
    def display_quet_dien_thoai_return(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_giam_thi_menu)
        self.uic.show_devices_sl.setText("")
        self.uic.show_list_devises.setText("Danh sách thiết bị quét được là:")

    #MÀN HÌNH GIÁM THỊ
    def display_quet_dien_thoai(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_quet_dien_thoai)



    #Dừng giám sát rộng
    def detect_far_stop(self):
        self.thread[6].stop()
        self.uic.btn_detect_far_start.setEnabled(True)
        self.uic.btn_giam_sat_rong_return.setEnabled(True)
        self.uic.btn_giam_sat_rong_close.setEnabled(True)
        self.uic.input_detect_far_camera.setPixmap(QPixmap("Image/bia_zalo.png"))
        self.uic.input_detect_far_camera.setScaledContents(True)




    #MÀN HÌNH GIÁM SÁT RỘNG
    def option_link(self):
        link_data = QFileDialog.getOpenFileName(filter="*.mp4 *.mov *.mkv")
        self.uic.input_detect_far_link.setText(link_data[0])

    #QUA MÀN HÌNH ĐIỂM DANH BẰNG MÃ QR
    def display_qr_code(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_attendace)


    #QUA MÀN HÌNH ĐIỂM DANH BẰNG KHUÔN MẶT
    # def display_diem_danh_khuon_mat(self):
    #      self.uic.main_widget.setCurrentWidget(self.uic.display_attendance_face_detect)



    #MÀN HÌNH GIÁM SÁT RỘNG
    def display_giam_sat_rong(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_giam_sat_rong)



    #MÀN HÌNH HỌC SINH
    def display_hoc_sinh(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_menu_student)


    #HÀM Ở MÀN HÌNH CHỌN MÔN HỌC
    def sl_toan(self):
        self.uic.input_detec_subject.setText("Toán")
    def sl_vat_li(self):
        self.uic.input_detec_subject.setText("Vật lí")
    def sl_hoa_hoc(self):
        self.uic.input_detec_subject.setText("Hoá học")
    def sl_sinh_hoc(self):
        self.uic.input_detec_subject.setText("Sinh học")
    def sl_tieng_anh(self):
        self.uic.input_detec_subject.setText("Tiếng anh")
    def sl_ngu_van(self):
        self.uic.input_detec_subject.setText("Ngữ văn")
    def sl_dia_li(self):
        self.uic.input_detec_subject.setText("Địa lí")
    def sl_GDCD(self):
        self.uic.input_detec_subject.setText("GDCD")
    def sl_lich_su(self):
        self.uic.input_detec_subject.setText("Lịch sử")
    def sl_mi_thuat(self):
        self.uic.input_detec_subject.setText("Mĩ thuật")
    def sl_am_nhac(self):
        self.uic.input_detec_subject.setText("Âm nhạc")
    def sl_gdqp(self):
        self.uic.input_detec_subject.setText("KHTN")
    def sl_td(self):
        self.uic.input_detec_subject.setText("Thể dục")
    def sl_tin_hoc(self):
        self.uic.input_detec_subject.setText("Tin học")
    def sl_tin_hoc_nghe(self):
        self.uic.input_detec_subject.setText("Ngoại Ngữ 2")






    #Hàm gửi mã qr  
    def save_qr_send(self):
        # Thêm thư viện qr code
        name = self.uic.input_data_name.text()
        sbd = self.uic.input_data_sbd.text()
        school = self.uic.input_data_school.text()
        class_hs = self.uic.input_data_class.text()
        make_qr_send_telegram(name,sbd,school,class_hs)
        self.uic.input_screen_image_2.setPixmap(QPixmap("QR_code.png"))
        self.uic.input_screen_image_2.setScaledContents(True)


    #Hàm qua màn hình môn học
    def display_subject(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_subject)

    #Từ màn hình môn học trở về màn hình giám sát
    def display_giam_sat(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_detec)





    #MÀN HÌNH CÀI ĐẶT THỜI GIAN
    #Hàm mở nội dung
    def open_folder_time(self):
        import webbrowser
        path = "Time_setup"
        webbrowser.open(path)
    #Hàm xoá nội dung
    def clear_content_input(self):
        self.uic.input_setup_time_schools.setText("")
        self.uic.input_setup_time_class.setText("")
        self.uic.input_setup_time_hours.setText("")
        self.uic.input_setup_time_minutes.setText("")

    #Hàm tạo file chứa thời gian
    def creat_file_time(self):
        name_schools = xu_li_ten_truong(self.uic.input_setup_time_schools.text())
        name_class = self.uic.input_setup_time_class.text()
        hour = int(self.uic.input_setup_time_hours.text())
        minute = int(self.uic.input_setup_time_minutes.text())
        print(f"{name_schools}-{name_class}-{hour}-{minute}")
        buoi = self.uic.btn_buoi.text()
        if buoi == "Buổi sáng":
            buoi_trong = "morning"
        else:
            buoi_trong = "afternoon"
        print("Buổi trong ngày là",buoi_trong)
        if buoi == "Buổi chiều" and hour <= 12:
            hour += 12
        else:
            pass
        #Ghi nội dung thời gian
        f = open(f"Time_setup/{name_schools}_{name_class}_{buoi_trong}.txt",mode = "w+",encoding="utf-8-sig")
        f.write(f"{hour},{minute}")
        f.close()
    #Chuyen sang màn hình tạo thời gian
    def display_setup_time(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_set_up_time)
    #Từ màn hình tạo thời gian chuyển về màn hình menu thời gian
    def return_display_time(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_diem_danh_menu)
    #Hàm điều chỉnh thời gian
    def mode_time_set(self):
        data = self.uic.btn_buoi.text()
        print("Dữ liệu là",data)
        if data == "Buổi sáng":
            print("Buổi sáng sang buổi chiều")
            self.uic.btn_buoi.setText("Buổi chiều")
            self.uic.btn_buoi.setStyleSheet("QPushButton#btn_buoi{\n"
            "border-radius: 15px;\n"
            "background-color: rgb(255, 170, 0);\n"
            "color: rgb(255, 255, 255);\n"
            "}\n"
            "\n"
            "QPushButton#btn_buoi:hover{\n"
            "border-radius: 15px;\n"
            "background-color:rgb(0, 170, 255);\n"
            "color: rgb(255, 255, 255);\n"
            "}")
        else:
            print("Buổi chiều chuyển sang buổi sáng")
            self.uic.btn_buoi.setText("Buổi sáng")
            self.uic.btn_buoi.setStyleSheet("QPushButton#btn_buoi{\n"
            "border-radius: 15px;\n"
            "background-color: rgb(0, 170, 255);\n"
            "color: rgb(255, 255, 255);\n"
            "}\n"
            "\n"
            "QPushButton#btn_buoi:hover{\n"
            "border-radius: 15px;\n"
            "background-color: rgb(255, 170, 0);\n"
            "color: rgb(255, 255, 255);\n"
            "}")


    #Chuyển từ màn hình tạo mã qr về màn hình tạo dữ liệu
    def display_create_data(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_attendance_make_data_face)
    #MÀN HÌNH ĐIỂM DANH MỚI
    def return_display_attendance(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_attendance_menu)
    #Hàm dừng điểm danh rộng
    def attendance_far_stop(self):
        self.thread[14].stop()
        #Set màn hình chính
        self.uic.screen_attendance_main.setPixmap(QPixmap("Image/main_screen.png"))
        self.uic.screen_attendance_main.setScaledContents(True)
        #Set thí sinh 1
        self.uic.screen_attendance_2.setPixmap(QPixmap("Image/KM.png"))
        self.uic.screen_attendance_2.setScaledContents(True)
        #Set thí sinh 2
        self.uic.screen_attendance_1.setPixmap(QPixmap("Image/QR.png"))
        self.uic.screen_attendance_1.setScaledContents(True)
        # self.uic.btn_mode_attendance.setEnabled(True)
    #Hàm khởi động điểm danh xa
    def start_attendace_far(self):
        self.thread[14] = Attendace_camera_far(index = 14)
        self.thread[14].start()
        self.thread[14].signal_main_far.connect(self.set_camera_main_attendance)
        self.thread[14].signal1_op_far.connect(self.set_camera_1_far)
        self.thread[14].signal2_op_far.connect(self.set_camera_2_far)
        self.thread[14].signal_data.connect(self.check_infor_faces)
        self.uic.btn_attendance_far_stop.setEnabled(True)
        # self.uic.btn_mode_attendance.setEnabled(False)
    #Hàm kiểm tra thông tin
    def check_infor_faces(self,data_student_list):
        list = data_student_list
        if len(list) != 0:
            self.uic.input_attendance_far_name.setText(list[0])
            #Set số báo danh
            self.uic.input_attendance_far_sbd.setText(list[1])
            #Set tên lớp
            self.uic.input_attendance_far_class.setText(list[3])
            #Set tên trường
            self.uic.input_attendance_far_school.setText(list[2])
        else:
            pass



    #Hàm set camera main
    def set_camera_main_attendance(self,cv_img):
        qt_img = convert_cv_qt_camera_main(cv_img)
        self.uic.screen_attendance_main.setPixmap(qt_img)  # Set ảnh lên màn hình
    #Hàm set camera 1 (Test)
    def set_camera_1_far(self,cv_img):
        qt_img = convert_cv_qt_camera_1_test(cv_img)  # Nhận dữ liệu truyền vô
        self.uic.screen_attendance_1.setPixmap(qt_img)  # Set ảnh lên màn hình
    #Hàm set camera 1 (Test)
    def set_camera_2_far(self,cv_img):
        qt_img = convert_cv_qt_camera_1_test(cv_img)  # Nhận dữ liệu truyền vô
        self.uic.screen_attendance_2.setPixmap(qt_img)  # Set ảnh lên màn hình









    #Hàm xoá nội dung ở màn hình đăng kí
    def clear_screen_dang_ki(self):
        self.uic.input_dang_ki_name.setText("")
        self.uic.input_dang_ki_user.setText("")
        self.uic.input_dang_ki_password.setText("")
        self.uic.input_dang_ki_password_re.setText("")
        self.uic.input_dang_ki_number_phone.setText("")
        self.uic.input_dang_ki_email.setText("")
        self.uic.mat_khau.setText("")





    #Hàm xoá nội dung ở màn hình điểm danh bằng khuôn mặt
    def clear_content_attendance_face(self):
        # self.uic.input_attendance_face_cam.setText("")
        self.uic.input_attendance_face_name.setText("")
        self.uic.input_attendance_face_sbd.setText("")
        self.uic.input_attendance_face_class.setText("")
        self.uic.input_attendance_face_school.setText("")
         #Dua ảnh lên màn hình điểm danh khuôn mặt
        self.uic.input_camera_attendance_face.setPixmap(QPixmap("Image/camera_dai.png"))
        self.uic.input_camera_attendance_face.setScaledContents(True)

    #Hàm xoá nội dung ở màn hình tạo dữ liệu khuôn mặt
    def make_data_face_clear_content(self):
        self.uic.input_data_cam.setText("")
        self.uic.input_id_face.setText("")
        self.uic.input_name_face.setText("")
        self.uic.input_sbd_face.setText("")
        self.uic.input_class_face.setText("")
        self.uic.input_school_face.setText("")
        #Dua ảnh lên màn hình điểm danh khuôn mặt
        self.uic.input_camera_make_data.setPixmap(QPixmap("Image/camera_dai.png"))
        self.uic.input_camera_make_data.setScaledContents(True)



    #Hàm dừng tạm thời micro
    def tam_dung_audio(self,kiem_tra):
        if kiem_tra == "Dung":
            self.thread[9].pause_stream()
        pass
    #Bật khả năng truy cập của micro
    def detect_audio_on(self):
        self.thread[9] = detect_audio(index = 9)
        self.thread[9].start()
    #Tắt khả năng truy cập
    def detect_audio_off(self):
        self.thread[9].stop()


    #Mở webhidro cacbon
    def open_hidro_cacbon(self):
        import webbrowser
        path = "https://chat.chatgptdemo.net/?ref=toolspedia.io"
        webbrowser.open(path)
    #Mở máy tính casio
    def open_casio(self):
        import webbrowser
        path = "https://lytuong.net/may-tinh-casio-online/"
        webbrowser.open(path)

    #Mở bảng tuần hoàn
    def open_bang_tuan_hoa(self):
        import webbrowser
        path = "https://ptable.com/?lang=vi#Properties"
        webbrowser.open(path)
    # Dạ đây ạ

    #Mở trang chủ
    def open_trang_chu_detect_fraud(self):
        import webbrowser
        path = "https://www.giamthiai.online"
        webbrowser.open(path)

    #Qua màn hình tiện ích
    def display_tien_ich(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_tien_ich_hs)

    #Mở link học sinh vi phạm
    def vinh_loi_hsvp(self):
        import webbrowser
        path = "https://web.telegram.org/k/#-4073345095"
        webbrowser.open(path)
    #Mở link mã qr học sinh
    def vinh_loi_maqrhs(self):
        import webbrowser
        path = "https://web.telegram.org/k/#-4057529611"
        webbrowser.open(path)
    #Mở qr điện thoại
    def vinh_loi_qrdt(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_vl)
    #Mở link học sinh vi phạm
    def tran_van_bay_hsvp(self):
        import webbrowser
        path = "https://web.telegram.org/k/#-4073345095"
        webbrowser.open(path)
    #Mở link mã QR
    def tran_van_bay_maqrhs(self):
        import webbrowser
        path = "https://web.telegram.org/k/#-4057529611"
        webbrowser.open(path)
    #Mở QR điện thoại
    def tran_van_bay_qrdt(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_tvb)
    #Mở link học sinh vi phạm
    def mai_thanh_the_hsvp(self):
        import webbrowser
        path = "https://web.telegram.org/k/#-4073345095"
        webbrowser.open(path)
    #Mở mã Qr học sinh
    def mai_thanh_the_maqrhs(self):
        import webbrowser
        path = "https://web.telegram.org/k/#-4057529611"
        webbrowser.open(path)
    #Mã QR điện thoại
    def mai_thanh_the_qrdt(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_mtt)
    #Mở link học sinh vi phạm
    def le_van_tam_hsvp(self):
        import webbrowser
        path = "https://web.telegram.org/k/#-4073345095"
        webbrowser.open(path)
    #Mở link mã Qr
    def le_van_tam_maqrhs(self):
    #Mở link diện thoại
        import webbrowser
        path = "https://web.telegram.org/k/#-4057529611"
        webbrowser.open(path)
    def le_van_tam_qrdt(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_le_van_tam)


    #Hàm ghi dữ liệu vào file bot qr
    def ghi_nhan_data_token_qr(self):
        #Lấy token
        token = self.uic.input_token_qr.text()
        #Lấy ID
        id = self.uic.input_id_qr.text()
        #Lấy tên trường
        truong = self.uic.input_qr_name_schools.text()
        schools = xu_li_ten_truong(truong)
        #Ghi nhận id và token vào file
        f = open(f"Telegram_bot/bot_qr_{schools}.txt",mode = "w+", encoding="utf-8-sig")
        chuoi = f"{token},{id},kt"
        f.write(chuoi)
        f.close()

    #GHI DỮ LIỆU VÀO FILE BOT MAIL
    def ghi_bot_mail(self):
        #Lấy Token
        token = self.uic.input_token_student.text()
        #Lấy ID
        id = self.uic.input_id_student.text()
        #Lấy tên trường
        schools = self.uic.input_student_name_schools.text()
        #Xử lí tên trường
        #Xử lí tên trường
        schools = xu_li_ten_truong(schools)
        print(schools)
        print("Token và id là",token)
        print(id)
        f = open(f"Telegram_bot/bot_mail_{schools}.txt",mode = "w+",encoding="utf-8-sig")
        f.write(f"{token},{id},x")
        f.close()

    #Từ màn hình giám sát qua màn hình bot email
    def display_bot_email(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_bot_student)
    #HÀM DỮ LIỆU

    #Hàm dừng camera ở màn hình điểm danh bằng mã QR
    def stop_camera_qr(self):
        self.thread[2].stop()






    #Hàm xoá màn hình
    def clear_screen_detect_far(self):
        #Set màn hình chính
        self.uic.screen_main.setPixmap(QPixmap("Image/main_screen.png"))
        self.uic.screen_main.setScaledContents(True)
        #Set thí sinh 1
        self.uic.screen_1.setPixmap(QPixmap("Image/TS_1.png"))
        self.uic.screen_1.setScaledContents(True)
        #Set thí sinh 2
        self.uic.screen_2.setPixmap(QPixmap("Image/TS_2.png"))
        self.uic.screen_2.setScaledContents(True)


    #Hàm dừng giám sát rộng
    def stop_detect_far(self):
        self.thread[10].stop()
        #Mở lại nút mở camera

        self.uic.btn_detect_far_open_camera.setEnabled(True)
        self.uic.input_cam_2ng.setEnabled(True)
        #Mở lại nút chuẩn bị
        self.uic.btn_detect_far_ready.setEnabled(True)
        #Mở lại nút bắt đầu
        self.uic.btn_detect_far_start_detect_new.setEnabled(True)
        #Nút vô hiệu hoá nút dừng
        self.uic.btn_detect_far_stop.setEnabled(False)
    #Hàm mở camera để test
    def open_camera_detect_far(self):
        #Vô hiệu hoá nút mở camera
        self.uic.btn_detect_far_open_camera.setEnabled(False)
        self.uic.input_cam_2ng.setEnabled(False)
        idx = 0
        try:
            idx = int(self.uic.input_cam_2ng.text())
            print(idx)
        except:
            print("Chỉ số cam phải là số nguyên, chuyển về cam 0")
            pass
        #Mở lại nút chuẩn bị
        self.uic.btn_detect_far_ready.setEnabled(True)

        self.thread[11] = Open_Camera(index=idx)
        self.thread[11].start()
        #Set camera chính
        self.thread[11].signal_main_op.connect(self.set_camera_main)
        # #Set camera bên trái
        self.thread[11].signal1_op.connect(self.set_camera_1)
        # #Set camera bên phải
        self.thread[11].signal2_op.connect(self.set_camera_2)

    #Hàm khởi chạy việc giám sát
    def start_detect_far_new(self):
        #Vô hiệu hoá nút bắt đầu
        self.uic.btn_detect_far_start_detect_new.setEnabled(False)
        #Nút vô hiệu hoá mở camera
        self.uic.btn_detect_far_open_camera.setEnabled(False)
        self.uic.input_cam_2ng.setEnabled(False)
        #Nút vô hiệu hoá nút chuẩn bị
        self.uic.btn_detect_far_ready.setEnabled(False)
        #Mở nút dừng
        self.uic.btn_detect_far_stop.setEnabled(True)

        idx = 0
        try:
            idx = int(self.uic.input_cam_2ng.text())
            print(idx)
        except:
            print("Chỉ số cam phải là số nguyên, chuyển về cam 0")
            pass

        self.thread[10] = Camera_new(index = idx)
        self.thread[10].start()
        self.thread[10].signal_main_far.connect(self.show_camera_main)
        self.thread[10].signal1_far.connect(self.show_camera_1)
        self.thread[10].signal2_far.connect(self.show_camera_2)




    #Hàm từ màn hình lựa chọn điểm danh, tạo dữ liệu qua màn hình lựa chọn điểm danh
    def display_menu_diem_danh_new(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_attendance_menu)




    #Hàm dừng camera của giám sát rộng
    def stop_camera_detect_far_test(self):
        #Mở nút bắt đầu
        self.uic.btn_detect_far_start_detect_new.setEnabled(True)
        #Mở nút mở camera
        self.uic.btn_detect_far_open_camera.setEnabled(True)
        self.uic.input_cam_2ng.setEnabled(True)
        self.thread[11].stop()

    #Các hàm để đưa ảnh lên
    #Hàm set camera main
    def set_camera_main(self,cv_img):
        qt_img = convert_cv_qt_camera_main(cv_img)
        self.uic.screen_main.setPixmap(qt_img)  # Set ảnh lên màn hình

    #Hàm set camera 1 (Test)
    def set_camera_1(self,cv_img):
        qt_img = convert_cv_qt_camera_1_test(cv_img)  # Nhận dữ liệu truyền vô
        self.uic.screen_1.setPixmap(qt_img)  # Set ảnh lên màn hình

    #Hàm set camera 2 (Test)
    def set_camera_2(self,cv_img):
        qt_img = convert_cv_qt_camera_2(cv_img)  # Nhận dữ liệu truyền vô
        self.uic.screen_2.setPixmap(qt_img)  # Set ảnh lên màn hình

    #Hàm show camera 1
    def show_camera_1(self,cv_img):
        qt_img = convert_cv_qt_camera_1(cv_img)  # Nhận dữ liệu truyền vô
        self.uic.screen_1.setPixmap(qt_img)  # Set ảnh lên màn hình
    #Hàm show camera 2
    def show_camera_2(self,cv_img):
        qt_img = convert_cv_qt_camera_2(cv_img)
        self.uic.screen_2.setPixmap(qt_img)  # Set ảnh lên màn hình

    #Hàm show camera 3
    def show_camera_main(self,cv_img):

        qt_img = convert_cv_qt_camera_main(cv_img)
        self.uic.screen_main.setPixmap(qt_img)  # Set ảnh lên màn hình


    # Hàm xoá dữ liệu ở màn hình make data
    def clear_data_in_make_qr(self):
        self.uic.input_data_name.setText("")
        self.uic.input_data_sbd.setText("")
        self.uic.input_data_school.setText("")
        self.uic.input_data_class.setText("")
        self.uic.input_screen_image_2.setPixmap(QPixmap("Image/take_qr.jpg"))
        self.uic.input_screen_image_2.setScaledContents(True)
    # Học sinh vi phạm
    def open_data_base_hsvp(self):
        import webbrowser
        path = "https://web.telegram.org/k/#-4073345095"
        webbrowser.open(path)

    # Hàm mở telegram
    def open_thong_bao(self):
       #Từ màn hình quản lí học sinh sang màn hình thông báo
        self.uic.main_widget.setCurrentWidget(self.uic.display_thong_bao)


    # Hàm mở cơ sở dữ liệu qr
    def open_data_base_qr(self):
        import webbrowser
        path = "https://web.telegram.org/k/#-4057529611"
        webbrowser.open(path)

    # Hàm clear màn hình đăng nhập
    def xoa_content_dang_nhap(self):
        self.uic.input_dang_nhap_user.setText("")
        self.uic.input_dang_nhap_pass.setText("")
        self.uic.dang_nhap.setText("")

    # Hàm clear màn hình
    def clear_man_hinh(self):
        #Đưa hình lên màn ảnh
        self.uic.screen_detec_camera.setPixmap(QPixmap("Image/camera_screen.png"))
        self.uic.screen_detec_camera.setScaledContents(True)
        #Tắt nút bắt đầu
        self.uic.btn_detec_start.setEnabled(False)
        #Bật lại nút bot mail
        self.uic.btn_detec_bot_telegram.setEnabled(True)
        # Bật lại các nút
        self.uic.btn_detect_menu_return.setEnabled(True)
        # Bật lại các thanh nhập nội dung
        self.uic.input_cam.setEnabled(True)
        self.uic.input_detec_name.setEnabled(True)
        self.uic.input_detec_sbd.setEnabled(True)
        self.uic.input_detec_school.setEnabled(True)
        self.uic.input_detec_class.setEnabled(True)
        self.uic.input_detec_subject.setEnabled(True)
        self.uic.btn_select_subject.setEnabled(True)
        self.uic.input_detec_name.setText("")
        self.uic.input_detec_sbd.setText("")
        self.uic.input_detec_school.setText("")
        self.uic.input_detec_class.setText("")
        self.uic.input_detec_subject.setText("")
        #Set lại nội dung ở trạng thái
        self.uic.trang_thai.setText("Trạng thái: Chuẩn bị làm bài")

    # Hàm xoá nội dung trong màn hình quên mật khẩu
    def xoa_content_quen_mk(self):
        self.uic.input_quen_mk_name.setText("")
        self.uic.input_quen_mk_user.setText("")
        self.uic.input_quen_mk_pass.setText("")
        self.uic.input_quen_mk_email.setText("")
        self.uic.input_quen_mk_pass_lay_lai.setText("")

    # Hàm lấy lại mật khẩu
    def lay_lai_mat_khau(self):
        # Lấy tên đăng nhập
        user = self.uic.input_quen_mk_user.text()

        # Ta khoản email
        mail_tk = self.uic.input_quen_mk_email.text()

        # Đọc dữ liệu từ cơ sở dữ liệu
        gs = gspread.service_account("token_gen_10012023.json")  # Truyền nguồn dữ liệu
        sht = gs.open_by_key("1_58RMWrl4Mj4CV4xJkNnml-nRTzMlydimEo1XzQwdyQ")
        #Mẫu dự phòng cơ sở dữ liệu
        # gs = gspread.service_account("key_du_phong_hoc_sinh.json")
        # sht = gs.open_by_key("1y4stYBt3lTCaJ-WYKC3-NYiuMZPvz9sWAUWwmLlBRN4")
        print(sht.title)
        worksheet = sht.get_worksheet(0)
        # Đọc nội dung cột email
        # Lấy cột tên đăng nhập
        ten_dang_nhap = worksheet.col_values(2)
        # Lấy email
        email_tk = worksheet.col_values(5)
        mat_khau = worksheet.col_values(3)
        print(email_tk)

        print("Tên đăng nhập ", ten_dang_nhap)
        if user in ten_dang_nhap:
            if mail_tk in email_tk:
                vitri = email_tk.index(mail_tk)
                mat_khau_new = mat_khau[vitri]
                self.uic.input_quen_mk_pass_lay_lai.setText(f"Mật khẩu là: {mat_khau_new}")  # Lấy lại mật khẩu
            else:
                self.uic.input_quen_mk_pass_lay_lai.setText("Email xác thực không tồn tại. Xin thử lại !!")
        else:
            self.uic.input_quen_mk_pass_lay_lai.setText("Tên đăng nhập không tồn tại. Xin thử lại !!")

    # Thoát trong màn hình giám sát
    def close_giam_sat(self):
        # Kiểm tra dữ liệu học sinh đã nhập chưa
        name = self.uic.input_detec_name.text()
        print(name)
        if name != "":
            # Ghi nội dung file google sheets
            import datetime
            import gspread
            from xoa_tieng_viet import no_accent_vietnamese
            gs = gspread.service_account("token_gen_10012023.json")  # Truyền nguồn dữ liệu
            # sht = gs.open_by_key("1NfVvEe3zvqQf_E0WJKPzOjXFLMwaeLGSVoJztPdmjV0")
            sht = gs.open_by_key("1Zb8mKW9TAwOIAJXyXopS_ldpPcStT7G6Zno0SOJm2QI")
            #Mẫu link dự phòng đang test
            # gs = gspread.service_account("key_du_phong_hoc_sinh.json")
            # sht = gs.open_by_key("1c_QPw7y1lqDFe9bp1bzMmU53p56UeW1utzFKcz3OIzs")

            print(sht.title)  # In tiêu đề ra
            worksheet = sht.get_worksheet(0)  # Truy cập vào học sinh vi phạm
            # Kiểm tra xem trong file có nội dung không
            col_test = worksheet.col_values(1)  # Lấy giá trị dòng
            # Nếu mảng trống thì ghi tiêu đề vào
            print(len(col_test))
            if len(col_test) == 0:
                tieu_de = ["Tên học sinh", "Số báo danh", "Tên trường", "Phòng thi", "Thời gian", "Ngày/Tháng/Năm",
                           "Nội dung vi phạm","Môn thi"]
                so_tieu_de = ["A1", "B1", "C1", "D1", "E1", "F1", "G1","H1"]
                # Ghi tiêu đề vào file
                for i in range(8):
                    worksheet.update_acell(so_tieu_de[i], tieu_de[i])  # Ghi file
                    worksheet.format("A1:H1", {
                        "horizontalAlignment": "CENTER",
                        "textFormat": {
                            "fontSize": 13,
                            "bold": True
                        }
                    })
            else:
                pass
            worksheet.format("A2:H800", {"horizontalAlignment": "CENTER", "textFormat": {"fontSize": 13, }})
            col_test = worksheet.col_values(1)  # Lấy giá trị dòng
            # Truy cập vào dòng khả thi
            row_empty = len(col_test) + 1
            index_content = ["A", "B", "C", "D", "E", "F", "G","H"]
            print("Dòng khả thi:", row_empty)
            # Khai báo mảng thông tin
            mang_thong_tin = []
            # Lấy content
            # Lấy tên
            name = self.uic.input_detec_name.text()
            # Lấy số báo danh
            sbd = self.uic.input_detec_sbd.text()
            # Lấy tên trường
            schools = self.uic.input_detec_school.text()
            # Lấy tên lớp
            class_name = self.uic.input_detec_class.text()
            #Lấy môn học
            subject = self.uic.input_detec_subject.text()
            # Lấy thời gian hiện tại
            thoi_gian = datetime.datetime.now()
            # Lấy giờ
            gio = thoi_gian.hour
            # Lấy phút
            phut = thoi_gian.minute
            # Lấy giây
            giay = thoi_gian.second
            # Lấy ngày
            ngay = thoi_gian.day
            # Lấy tháng
            thang = thoi_gian.month
            # Lấy năm
            nam = thoi_gian.year
            thoi_gian_lam_bai = f"{gio}:{phut}:{giay}"
            vao_luc = f"{ngay}/{thang}/{nam}"
            # Thêm nội dung vào mảng vừa tạo
            # Thêm tên
            mang_thong_tin.append(name)
            # Thêm số báo danh
            mang_thong_tin.append(sbd)
            # Thêm tên trường
            mang_thong_tin.append(schools)
            # Thêm lớp
            mang_thong_tin.append(class_name)
            # Thêm thời gian vào làm bài
            mang_thong_tin.append(thoi_gian_lam_bai)
            # Thêm ngày tháng làm bài
            mang_thong_tin.append(vao_luc)
            loaihinh = "Tự ý đóng chương trình giám sát"
            # Thêm nội dung vào mảng
            mang_thong_tin.append(loaihinh)
            #Thêm môn thi
            mang_thong_tin.append(subject)
            for i in range(8):
                so_chi_muc = f"{index_content[i]}{row_empty}"
                worksheet.update_acell(so_chi_muc, mang_thong_tin[i])
            else:
                pass
            print('Học sinh tự ý thoát chương trình')
            QApplication.instance().quit()

        else:
            print("Học sinh đã kết thúc làm bài")
            QApplication.instance().quit()

    # HÀM
    # Hàm sang màn hình học sinh
    def display_student(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_menu_student)

    # Hàm từ màn hình giám sát trở về màn hình học sinh
    def display_student_return(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_giam_sat_menu)

    # Hàm từ màn hình học sinh qua màn hình giám sát diện rộng
    def display_detect_far(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_far_detect)

    # Hàm chọn dữ liệu cho giám sát diện rộng
    def chosen_link_data(self):
        link_data_input = QFileDialog.getOpenFileName(filter="*.mp4 *.mkv")
        self.uic.input_detect_far_link.setText(link_data_input[0])

    # Hàm giám sát diện rộng
    # Hàm bắt đầu nhận dạng từ xa
    def detect_far_start(self):
        cam_link = self.uic.input_detect_far_link.text()
        f = open("link_camera/link_data_camera.txt", mode="w+", encoding="utf-8-sig")
        f.write(f"{cam_link}")
        f.close()

        # self.thread[6] = detect_far(index=6)
        self.thread[6] = CameraDetectionThread()

        self.thread[6].start()
        # Kết nối với tín hiệu
        self.thread[6].signal6.connect(self.show_cam_detect_far)
        # Vô hiệu hoá nút bắt đầu
        self.uic.btn_detect_far_start.setEnabled(False)
        # Bật lại nút bắt đầu
        self.uic.btn_giam_sat_rong_stop.setEnabled(True)
        # Vô hiệu hoá nút trở về
        self.uic.btn_giam_sat_rong_return.setEnabled(False)
        # Vô hiệu hoá nút thoát
        self.uic.btn_giam_sat_rong_close.setEnabled(False)

    # Hàm set ảnh lên màn hình giám sát
    # SHOW CAM NHẬN DẠNG
    def show_cam_detect_far(self, cv_img):
        qt_img = convert_cv_qt_far(cv_img)  # Nhận dữ liệu truyền vô
        self.uic.input_detect_far_camera.setPixmap(qt_img)  # Set ảnh lên màn hình

    # Hàm từ màn hình menu sang màn hình giáo viên
    def display_teacher(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_xac_nhan_giam_thi)

    # Hàm xác nhận giám thị
    def verification_teacher(self):

        ma_xn = self.uic.input_verification.text()
        if ma_xn == "1234" or ma_xn == "0000":
            self.uic.main_widget.setCurrentWidget(self.uic.display_giam_thi)
            self.uic.input_verification.setText("")
        else:
            self.uic.ma_xac_nhan.setText("Mã xác nhận không chính xác. Vui lòng nhập lại")

    # Hàm trở về màn hình xác nhận mã
    def display_xac_nhan(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_xac_nhan_giam_thi)

    # Hàm qua màn hình đăng kí tài khoản
    def display_dang_ki_tai_khoan(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_dang_ki)

    # Hàm qua màn hình giám thị
    def display_giam_thi(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_giam_thi)

    # Hàm qua màn hình đăng nhập
    def display_dang_nhap_tk(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_dang_nhap)

    # Hàm quên mật khẩu trong màn hình đăng nhập
    def quen_mat_khau(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_forget_pass)




    # Đăng kí tài khoản giám thị
    def dang_ki_tai_khoan(self):
        # Lấy tên hiển thị
        name = self.uic.input_dang_ki_name.text()
        # Lấy tên đăng nhập
        user = self.uic.input_dang_ki_user.text()
        # Lấy mật khẩu
        password = self.uic.input_dang_ki_password.text()
        # Lấy mật khẩu lần 2
        password_re = self.uic.input_dang_ki_password_re.text()
        # Lấy số điện thoại
        number_phone = self.uic.input_dang_ki_number_phone.text()
        # Lấy email
        email_khach = self.uic.input_dang_ki_email.text()
        mang_thong_tin = []
        # Thêm tin vào mảng
        mang_thong_tin.append(name)  # 1
        # Thêm tên đăng nhập vào mảng
        mang_thong_tin.append(user)  # 2
        # Thêm mật khẩu vào mảng
        mang_thong_tin.append(password)  # 3
        # Thêm số điện thoại vào mảng
        mang_thong_tin.append(number_phone)  # 4
        # Thêm email vào mảng
        mang_thong_tin.append(email_khach)  # 5
        thoi_gian = datetime.datetime.now()
        # Lấy ngày hiện tại
        ngay = thoi_gian.day
        # Lấy tháng hiện tại
        thang = thoi_gian.month
        # Lấy năm hiện tại
        nam = thoi_gian.year
        time_ghi = f"{ngay}-{thang}-{nam}"
        mang_thong_tin.append(time_ghi)  # 6
        # Đọc dữ liệu từ cơ sở dữ liệu
        gs = gspread.service_account("token_gen_10012023.json")  # Truyền nguồn dữ liệu
        sht = gs.open_by_key("1_58RMWrl4Mj4CV4xJkNnml-nRTzMlydimEo1XzQwdyQ")
        #Mẫu dự phòng cơ sở dữ liệu
        # gs = gspread.service_account("key_du_phong_hoc_sinh.json")
        # sht = gs.open_by_key("1y4stYBt3lTCaJ-WYKC3-NYiuMZPvz9sWAUWwmLlBRN4")
        print(sht.title)
        worksheet = sht.get_worksheet(0)
        # Thuật toán kiểm tra dữ liệu:

        # Kiểm tra xem trong file có nội dung không
        col_test = worksheet.col_values(1)  # Lấy giá trị dòng
        # Nếu mảng trống thì ghi tiêu đề vào
        if len(col_test) == 0:
            tieu_de = ["Tên giám thị", "Tên đăng nhập", "Mật khẩu", "Số điện thoại", "Email", "Ngày tạo tài khoản"]
            so_tieu_de = ["A1", "B1", "C1", "D1", "E1", "F1"]
            worksheet.format("A1:F5000", {"horizontalAlignment": "CENTER", })
            # Ghi tiêu đề vào file
            for i in range(6):
                worksheet.update_acell(so_tieu_de[i], tieu_de[i])  # Ghi file
            else:
                pass
        # Kiểm tra cột tên đăng nhập:
        col_user = worksheet.col_values(2)
        print("Cột đọc là", col_user)
        kiem_tra_tai_khoan = None
        print("Chạy lại cột")
        if user in col_user:
            # Tên đăng nhập bị trùng
            kiem_tra_tai_khoan = False
        else:
            kiem_tra_tai_khoan = True

        print("Kiểm tra là:", kiem_tra_tai_khoan)
        # Hàm ghi nội dung
        if kiem_tra_tai_khoan == True:
            if password != password_re:  # Nếu mật khẩu không khớp
                self.uic.mat_khau.setText("Mật khẩu vừa nhập không khớp. Vui lòng nhập lại !!")
            else:
                # Ghi tài khoản mật khẩu
                col_test = worksheet.col_values(1)  # Lấy giá trị dòng
                # Truy cập vào dòng khả thi
                row_empty = len(col_test) + 1
                index_content = ["A", "B", "C", "D", "E", "F"]
                for k in range(6):
                    so_chi_muc = f"{index_content[k]}{row_empty}"
                    worksheet.update_acell(so_chi_muc, mang_thong_tin[k])
                self.uic.mat_khau.setText("Đã tạo thành công tài khoản.")
            kiem_tra_tai_khoan = None

        else:
            self.uic.mat_khau.setText("Tên đăng nhập đã tồn tại. Vui lòng nhập tên khác !!!")
            kiem_tra_tai_khoan = None

    # Hàm quét điện thoại
    def scan_phone(self):
        #Set nội dungĐã tra
        self.uic.tinh_trang_quet.setText(" Đã quét thành công !")
        def get_local_ip():
            # Lấy địa chỉ IP của máy tính local
            ipconfig_output = subprocess.check_output(['ipconfig']).decode('utf-8')
            ip_pattern = r'IPv4 Address.*: (.*)\r\n'
            ip_match = re.search(ip_pattern, ipconfig_output)
            if ip_match:
                return ip_match.group(1)
            else:
                return None

        def get_devices_on_network():
            # Lấy danh sách các thiết bị trên cùng một mạng wifi
            nm = nmap.PortScanner()
            local_ip = get_local_ip()
            if local_ip:
                # Tạo biến để lưu trữ địa chỉ IP của mạng wifi hiện tại
                network_prefix = '.'.join(local_ip.split('.')[0:3]) + '.0/24'
                # Quét các thiết bị trong mạng wifi hiện tại
                nm.scan(hosts=network_prefix, arguments='-sn')
                # Trích xuất danh sách địa chỉ MAC của các thiết bị đã quét được
                mac_addresses = []
                for host in nm.all_hosts():
                    if 'mac' in nm[host]['addresses']:
                        mac_addresses.append(nm[host]['addresses']['mac'])
                return mac_addresses
            else:
                return None

        def get_connected_devices_on_wifi(ssid):
            # Lấy danh sách các thiết bị đang kết nối vào mạng wifi có tên là ssid
            nm = nmap.PortScanner()
            # Quét các thiết bị trong mạng wifi hiện tại
            nm.scan(hosts=ssid, arguments='-sn')
            # Trích xuất danh sách địa chỉ MAC của các thiết bị đã quét được
            mac_addresses = []
            for host in nm.all_hosts():
                if 'mac' in nm[host]['addresses']:
                    mac_addresses.append(nm[host]['addresses']['mac'])
            return mac_addresses

        # Sử dụng hàm để lấy danh sách các thiết bị trên cùng một mạng wifi
        devices_on_network = get_devices_on_network()
        # Hiển thị danh sách các thiết bị trên cùng một mạng wifi
        if devices_on_network:
            string = ""
            so = len(devices_on_network)
            self.uic.show_devices_sl.setText(f"Số thiết bị quét được là:{so}")
            for i in devices_on_network:
                string += f"{i} \n"
            self.uic.show_list_devises.setText(string)
            print("Số thiết bị xung quanh là:", len(devices_on_network))
            print('Danh sách các thiết bị trên cùng một wifi:')
            print("Địa chỉ máy là:", devices_on_network)
            for device in devices_on_network:
                print(device)

        else:
            self.uic.show_list_devises.setText("Không tìm thấy thiết bị")
            print('Không tìm thấy thiết bị nào trên mạng wifi hiện tại')
        # Sử dụng hàm để lấy danh sách các thiết bị đang kết nối vào mạng wifi
        connected_devices_on_wifi = get_connected_devices_on_wifi('wifi')

        # Hiển thị danh sách các thiết bị đang kết nối vào mạng wifi
        if connected_devices_on_wifi:
            print('Danh sách các thiết bị đang kết nối vào mạng wifi:')
            print("Địa chỉ máy là:", connected_devices_on_wifi)
            self.uic.tinh_trang_quet.setText("Đã quét thành công !")
            for device in connected_devices_on_wifi:
                print(device)







    # Hàm hoàn thành bài thi
    def hoan_thanh_bai_thi(self):
        #Tắt nút bắt đầu
        self.uic.btn_detec_start.setEnabled(False)
        noidung = self.uic.input_detec_name.text()
        #Bật lại nút bot mail
        self.uic.btn_detec_bot_telegram.setEnabled(True)
        # Bật lại các nút
        self.uic.btn_detect_menu_return.setEnabled(True)
        # Bật lại các thanh nhập nội dung
        self.uic.input_cam.setEnabled(True)
        self.uic.input_detec_name.setEnabled(True)
        self.uic.input_detec_sbd.setEnabled(True)
        self.uic.input_detec_school.setEnabled(True)
        self.uic.input_detec_class.setEnabled(True)
        self.uic.input_detec_subject.setEnabled(True)
        self.uic.btn_select_subject.setEnabled(True)
        if noidung != "":
            # Ghi nội dung file google sheets
            import datetime
            import gspread
            from xoa_tieng_viet import no_accent_vietnamese
            gs = gspread.service_account("token_gen_10012023.json")  # Truyền nguồn dữ liệu
            # sht = gs.open_by_key("1NfVvEe3zvqQf_E0WJKPzOjXFLMwaeLGSVoJztPdmjV0")
            sht = gs.open_by_key("1Zb8mKW9TAwOIAJXyXopS_ldpPcStT7G6Zno0SOJm2QI")
            #Mẫu link dự phòng đang test
            # gs = gspread.service_account("key_du_phong_hoc_sinh.json")
            # sht = gs.open_by_key("1c_QPw7y1lqDFe9bp1bzMmU53p56UeW1utzFKcz3OIzs")
            print(sht.title)  # In tiêu đề ra
            worksheet = sht.get_worksheet(0)  # Truy cập vào sheets lịch sử làm bài
            # Kiểm tra xem trong file có nội dung không
            col_test = worksheet.col_values(1)  # Lấy giá trị dòng
            # Nếu mảng trống thì ghi tiêu đề vào
            if len(col_test) == 0:
                tieu_de = ["Tên học sinh", "Số báo danh", "Tên trường", "Phòng thi", "Thời gian", "Ngày/Tháng/Năm",
                           "Nội dung","Môn thi"]
                so_tieu_de = ["A1", "B1", "C1", "D1", "E1", "F1", "G1","H1"]
                # Ghi tiêu đề vào file
                for i in range(8):
                    worksheet.update_acell(so_tieu_de[i], tieu_de[i])  # Ghi file
                    worksheet.format("A1:H1", {
                        "horizontalAlignment": "CENTER",
                        "textFormat": {
                            "fontSize": 13,
                            "bold": True
                        }
                    })
            else:
                pass
            worksheet.format("A2:H800", {"horizontalAlignment": "CENTER", "textFormat": {"fontSize": 13, }})
            col_test = worksheet.col_values(1)  # Lấy giá trị dòng
            # Truy cập vào dòng khả thi
            row_empty = len(col_test) + 1
            index_content = ["A", "B", "C", "D", "E", "F", "G","H"]
            print("Dòng khả thi:", row_empty)
            # Khai báo mảng thông tin
            mang_thong_tin = []
            # Lấy content
            # Lấy tên
            name = self.uic.input_detec_name.text()
            # Lấy số báo danh
            sbd = self.uic.input_detec_sbd.text()
            # Lấy tên trường
            schools = self.uic.input_detec_school.text()
            # Lấy tên lớp
            class_name = self.uic.input_detec_class.text()
            #Lấy tên môn thi
            subject = self.uic.input_detec_subject.text()
            # Lấy thời gian hiện tại
            thoi_gian = datetime.datetime.now()
            # Lấy giờ
            gio = thoi_gian.hour
            # Lấy phút
            phut = thoi_gian.minute
            # Lấy giây
            giay = thoi_gian.second
            # Lấy ngày
            ngay = thoi_gian.day
            # Lấy tháng
            thang = thoi_gian.month
            # Lấy năm
            nam = thoi_gian.year
            thoi_gian_lam_bai = f"{gio}:{phut}:{giay}"
            vao_luc = f"{ngay}/{thang}/{nam}"
            # Thêm nội dung vào mảng vừa tạo
            # Thêm tên
            mang_thong_tin.append(name)
            # Thêm số báo danh
            mang_thong_tin.append(sbd)
            # Thêm tên trường
            mang_thong_tin.append(schools)
            # Thêm lớp
            mang_thong_tin.append(class_name)
            # Thêm thời gian vào làm bài
            mang_thong_tin.append(thoi_gian_lam_bai)
            # Thêm ngày tháng làm bài
            mang_thong_tin.append(vao_luc)
            loaihinh = "Hoàn thành bài thi"
            # Thêm nội dung vào mảng
            mang_thong_tin.append(loaihinh)
            monthi = self.uic.input_detec_subject.text()
            mang_thong_tin.append(monthi)

            for i in range(8):
                so_chi_muc = f"{index_content[i]}{row_empty}"
                worksheet.update_acell(so_chi_muc, mang_thong_tin[i])
        else:
            pass
            # Xoá bỏ thông tin học sinh.
        # Xoá bỏ tên
        self.uic.input_detec_name.setText("")
        # Xoá bỏ số báo danh
        self.uic.input_detec_sbd.setText("")
        # Xoá bỏ tên trường
        self.uic.input_detec_school.setText("")
        # Xoá bỏ phòng thi
        self.uic.input_detec_class.setText("")
        #Xoá bỏ nội dung môn thi
        self.uic.input_detec_subject.setText("")
        self.thread[1].stop()
        self.thread[9].stop()
        # Set quá trạng thái
        self.uic.trang_thai.setText("Trạng thái: Hoàn thành bài thi")

    # Đăng nhập tài khoản giám thị
    def dang_nhap_tai_khoan(self):
        # Lấy tên đăng nhập
        user = self.uic.input_dang_nhap_user.text()
        # Lấy mật khẩu
        password = self.uic.input_dang_nhap_pass.text()
        # Đọc dữ liệu từ cơ sở dữ liệu
        gs = gspread.service_account("token_gen_10012023.json")  # Truyền nguồn dữ liệu
        sht = gs.open_by_key("1_58RMWrl4Mj4CV4xJkNnml-nRTzMlydimEo1XzQwdyQ")
        # self.uic.input_dang_nhap_user.setText("")
        # self.uic.input_dang_nhap_pass.setText("")
        #Mẫu dự phòng cơ sở dữ liệu
        # gs = gspread.service_account("key_du_phong_hoc_sinh.json")
        # sht = gs.open_by_key("1y4stYBt3lTCaJ-WYKC3-NYiuMZPvz9sWAUWwmLlBRN4")

        print(sht.title)
        worksheet = sht.get_worksheet(0)
        # Kiểm tra cột tên đăng nhập:
        col_user = worksheet.col_values(2)
        if user in col_user:
            col_pass = worksheet.col_values(3)  # Lấy cột mật khẩu
            print("Cột mật khẩu là", col_pass)
            if password in col_pass:
                # Xử lí mật khẩu
                vitri_user = col_user.index(user)  # Lấy vị trí mật khẩu
                mat_khau_tai_khoan = col_pass[vitri_user]
                print("Mật khẩu là", mat_khau_tai_khoan)
                print("Password là", password)
                if password == mat_khau_tai_khoan:
                    self.uic.main_widget.setCurrentWidget(self.uic.display_giam_thi_menu)
                else:
                    self.uic.dang_nhap.setText("Mật khẩu vừa nhập không chính xác. Vui lòng thử lại !!")


            else:
                self.uic.dang_nhap.setText("Mật khẩu vừa nhập không chính xác. Vui lòng thử lại !!")
        else:
            self.uic.dang_nhap.setText("Tên đăng nhập không tồn tại. Vui lòng thử lại")

    # Màn hình quản lí học sinh
    def display_qlhs(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_qlhs)

    # Qua màn hình quét điện thoại
    def display_quet_dien_thoai(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_quet_dien_thoai)

    # Qua màn hình giám thị
    def display_man_hinh_giam_thi(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_giam_thi_menu)

    # Qua màn hình quên mật khẩu
    def display_quen_mat_khau(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_forget_pass)

    # Nút mở cơ sở dữ liệu
    def co_so_du_lieu(self):
        import webbrowser
        path = "https://docs.google.com/spreadsheets/d/1Zb8mKW9TAwOIAJXyXopS_ldpPcStT7G6Zno0SOJm2QI/edit#gid=2044441802"
        webbrowser.open(path)

    # Qua màn hình thông tin tài khoản
    #def thong_tin_tai_khoan(self):
        # Nút chuyển sang màn hình thông tin tài khoản
        #self.uic.main_widget.setCurrentWidget(self.uic.display_thong_tin_tai_khoan)
        # Lấy tên đăng nhập
        #user = self.uic.input_dang_nhap_user.text()
        # Đọc dữ liệu từ cơ sở dữ liệu
        #gs = gspread.service_account("token_gen_10012023.json")  # Truyền nguồn dữ liệu
        #sht = gs.open_by_key("1_58RMWrl4Mj4CV4xJkNnml-nRTzMlydimEo1XzQwdyQ")
        #Mẫu dự phòng cơ sở dữ liệu
        # gs = gspread.service_account("key_du_phong_hoc_sinh.json")
        # sht = gs.open_by_key("1y4stYBt3lTCaJ-WYKC3-NYiuMZPvz9sWAUWwmLlBRN4")


        #print(sht.title)
        #worksheet = sht.get_worksheet(0)
        # Kiểm tra cột tên đăng nhập:
        #col_user = worksheet.col_values(2)
        #vi_tri = col_user.index(user)
       # print("Vị trí là:", vi_tri)
        #vi_tri = vi_tri + 1
        #row_thong_tin = worksheet.col_values(vi_tri)
        #print("Thông tin người dùng là", row_thong_tin)
        # Set tên hiển thị
       # self.uic.ten_hien_thi.setText(row_thong_tin[0])
        # Set tên đăng nhập
        #self.uic.ten_dang_nhap.setText(row_thong_tin[1])
        # Set mật khẩu
        #self.uic.mat_khau_tk.setText(row_thong_tin[2])
        # Set số điện thoại
        #self.uic.so_dien_thoai.setText(row_thong_tin[3])
        # Set gmail
        #self.uic.email.setText(row_thong_tin[4])

    # Hàm menu
    # Hàm qua màn hình QR txt
    def open_qr_bot(self):
       self.uic.main_widget.setCurrentWidget(self.uic.display_bot_qr_txt)

    # Hàm mở file token
    def open_token_txt(self):
        import webbrowser
        path = "Telegram_bot"
        webbrowser.open(path)

    # Hàm mở thư mục chứa học sinh giám sát
    def open_folder_giam_sat(self):
        import webbrowser
        path = "data_student"
        webbrowser.open(path)

    # Hàm mở thư mục chấm bài
    def open_foler_answer(self):
        import webbrowser
        path = "Ketqua"
        webbrowser.open(path)

    # ĐIỂM DANH BẰNG MÃ QR
    def qt_display_attendance_qr_return(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_attendance_menu)

    def qt_display_attendance_qr_menu_return(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_attendance_menu)

    # Mở thư mục chứa file điểm danh
    def open_folder_excel_qr(self):
        import webbrowser
        path = "Excel_qr"
        webbrowser.open(path)

    # ĐIỂM DANH BẰNG KHUÔN MẶT
    def qt_diplay_attendance_face(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_attendance_far)

    # Tạo dữ liệu khuôn mặt
    def qt_display_attendance_make_data_face(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_attendance_make_data_face)

    # Hàm chọn đường link video để chọn video
    def make_data_link(self):
        link_data_input = QFileDialog.getOpenFileName(filter="*.mp4 *.mkv")
        self.uic.input_data_cam.setText(link_data_input[0])

    # Hàm trở về màn hình điểm danh bằng khuôn mặt
    def qt_display_make_data_face_return(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_tao_du_lieu)

    # Nhận dạng khuôn mặt
    def start_detect_face(self):
        self.uic.btn_attendance_face_cam_stop.setEnabled(True)
        # Lấy dữ liệu link
        cam_link = self.uic.input_attendance_face_cam.text()
        f = open("link_camera/link_cam_detect.txt", mode="w+", encoding="utf-8-sig")
        f.write(f"{cam_link}")
        f.close()
        self.thread[4] = detect_face_class(index=4)
        self.thread[4].start()
        # Kết nối với tính hiệu
        self.thread[4].signal4.connect(self.show_cam_detect_face)
        # Truyen tín hiệu đi
        self.thread[4].signal5.connect(self.set_data_detect)

    # Xác nhận face
    # def xac_nhan_face(self):
    #     # self.thread[4].stop()
    #     # #Ghi file điểm danh
    #     # Lấy tên
    #     name = self.uic.input_attendance_face_name.text()
    #     # Lấy số báo danh
    #     sbd = self.uic.input_attendance_face_sbd.text()
    #     # Lấy lớp
    #     lop = self.uic.input_attendance_face_class.text()
    #     # Lấy tên trường
    #     truong = self.uic.input_attendance_face_school.text()
    #     # Thời gian
    #     thoigian = datetime.datetime.now()
    #     # Lấy ngày hiện tại
    #     ngay = thoigian.day
    #     # Lấy tháng hiện tại
    #     thang = thoigian.month
    #     # Lấy năm hiện tại
    #     nam = thoigian.year
    #     f_read = open(f"Excel_face/{lop}_{ngay}_{thang}_{nam}.csv", mode="a", encoding="utf-8-sig")
    #     f_read.close()
    #     f_read = open(f"Excel_face/{lop}_{ngay}_{thang}_{nam}.csv", mode="r", encoding="utf-8-sig")
    #     header = f_read.readline().strip()
    #     # print("Đầu dòng", header)
    #     f_read.close()
    #     if header == "":
    #         f = open(f"Excel_face/{lop}_{ngay}_{thang}_{nam}.csv", mode="w+", encoding="utf-8-sig")
    #         info = "Họ và tên,Số báo danh, Tên lớp, Tên trường, Điểm danh, Thời gian"
    #         f.write(f"{info} \n")
    #         # print("Ghi đè")
    #     else:
    #         # print("Ghi tiếp")
    #         f = open(f"Excel_face/{lop}_{ngay}_{thang}_{nam}.csv", mode="a", encoding="utf-8-sig")
    #     thoigian = datetime.datetime.now()
    #     gio = thoigian.hour
    #     phut = thoigian.minute
    #     diem_danh = ""
    #
    #     if gio <= 6 and phut <= 45:
    #         diem_danh = " "
    #     else:
    #         diem_danh = "Đi trễ"
    #     thoi_gian_now = f"{gio}:{phut}"
    #     # print("Thông tin học sinh", mang_xuli)
    #     row = f"{name},{sbd},{lop},{truong},{diem_danh},{thoi_gian_now} \n"
    #     print(row)
    #     f.write(row)
    #     f.close()
    #     mang_data = []
    #     # Thêm tên vào mảng data
    #     mang_data.append(name)
    #     # Thêm số báo danh
    #     mang_data.append(sbd)
    #     # Thêm tên trường vào mảng data
    #     mang_data.append(truong)
    #     # Thêm tên lớp vào mảng data
    #     mang_data.append(lop)
    #     # Thêm cái ngày hiện tại vô
    #     thoi_gian = datetime.datetime.now()
    #     # Lấy ngày hiện tại
    #     ngay = thoi_gian.day
    #     # Lấy tháng hiện tại
    #     thang = thoi_gian.month
    #     # Lấy năm hiện tại
    #     nam = thoi_gian.year
    #     # Tạo thời gian
    #     ngay_thang = f"{ngay}/{thang}/{nam}"
    #
    #     set_info_diem_danh_google_sheets(mang_data, diem_danh, thoi_gian_now, ngay_thang)

    # Hàm show thư mục chứa ảnh
    def show_folder_img_face(self):
        import webbrowser
        path = "dataset"
        webbrowser.open(path)

    # Hàm show thư mục chứa model
    def show_folder_model(self):
        import webbrowser
        path = "info_student"
        webbrowser.open(path)

    # Hàm trích xuất dữ liệu trong tạo dữ liệu
    def make_data_export_data(self):
        # Lấy dữ liệu từ các ô
        # Nguồn dữ liệu
        input_video = self.uic.input_data_cam.text()
        # ID học sinh
        input_id = self.uic.input_id_face.text()
        # Tên học sinh
        input_name = self.uic.input_name_face.text()
        # Số báo danh
        input_sbd = self.uic.input_sbd_face.text()
        # Lớp
        input_class = self.uic.input_class_face.text()
        # Tên trường
        input_school = self.uic.input_school_face.text()
        f = open(f"link_camera/link_cam_set.txt", mode="w+", encoding="utf-8-sig")
        f.write(f"{input_video}")
        f.close()
        f = open("link_camera/id.txt", mode="w+", encoding="utf-8-sig")
        f.write(f"{input_id}")
        f.close()
        print("Đã lấy xong dữ liệu")
        # Ghi tên file
        f = open(f"info_student/{input_id}_{input_name}_{input_class}.txt", mode="w+", encoding="utf-8-sig")
        # GHi nội dung
        f.write(f"{input_video} \n"
                f"{input_id} \n"
                f"{input_name}\n"
                f"{input_sbd}\n"
                f"{input_class}\n"
                f"{input_school}")
        f.close()

        # Tạo file để chứa thông tin
        f_read = open(f"info_student/model.csv", mode="a", encoding="utf-8-sig")
        f_read.close()
        # Kiểm tra dữ liệu trong file
        f_read = open(f"info_student/model.csv", mode="r", encoding="utf-8-sig")
        header = f_read.readline().strip()
        f_read.close()
        # Kiểm tra xem trong file đã có nội dung chưa
        if header == "":
            f = open(f"info_student/model.csv", mode="w+", encoding="utf-8-sig")
            info = "ID học sinh, Họ và tên,Số báo danh, Tên lớp,Tên trường, Tên hiển thị"
            f.write(f"{info} \n")
        else:
            f = open(f"info_student/model.csv", mode="a", encoding="utf-8-sig")
        ten_hien_thi = no_accent_vietnamese(input_name)
        print("Trước khi ghi nội dung")
        f.write(f"{input_id},{input_name},{input_sbd},{input_class},{input_school},{ten_hien_thi} \n")
        print("Đã ghi nội dung xong")
        f.close()

        #Xử lí tên trường và ghi
        ten_truong = xu_li_ten_truong(input_school)
        f = open("Telegram_bot/schools.txt",mode = "w+",encoding="utf-8-sig")
        f.write(f"{ten_truong}")
        f.close()



        #Hàm gửi mã qr đi
        make_qr_send(input_name, input_sbd, input_school,input_class)




    # Cập nhật dữ liệu khuôn mặt
    def qt_display_attendance_update_data_face(self):
        self.uic.main_widget.setCurrentWidget(self.uic.diplay_attendance_update_data_face)
        # Cập nhật dữ liệu
        f = open("time_update/thoigian.txt", mode="r", encoding="utf-8-sig")
        time_update = f.readline().strip()
        self.uic.time_data_update.setText(f"Lần cập nhật gần nhất vào ngày: {time_update}")

    # Điểm danh bằng khuôn mặt
    def qt_display_attendance_face(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_attendance_far)

    # Nút trở về màn hình điểm danh menu
    def qt_display_attendance_menu_return(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_attendance_menu)

    # Nút trở về màn hình cập nhật dữ liệu khuôn mặt
    def attendance_update_data_return(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_diem_danh_menu)

    # ĐIỂM DANH BẰNG KHUÔN MẶT
    # Nút trở về màn hình điểm danh bằng khuôn mặt
    def qt_attendance_face_return(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_attendance_face)

    # Hàm chọn link cho cam nhận dạng
    def link_face_detect(self):
        link_cam = QFileDialog.getOpenFileName(filter="*.mp4 *.mkv *.png")
        self.uic.input_attendance_face_cam.setText(link_cam[0])

    # SHOW CAM NHẬN DẠNG
    def show_cam_detect_face(self, cv_img):
        qt_img = convert_cv_qt(cv_img)  # Nhận dữ liệu truyền vô
        self.uic.input_camera_attendance_face.setPixmap(qt_img)  # Set ảnh lên màn hình

    # SET dữ liệu lên mảng
    def set_data_detect(self, data_detect):
        print("Mảng vừa nhận được là", data_detect)
        # SET tên
        self.uic.input_attendance_face_name.setText(data_detect[0])
        # Set số báo danh
        self.uic.input_attendance_face_sbd.setText(data_detect[1])
        # SET lớp
        self.uic.input_attendance_face_class.setText(data_detect[2])
        # Set trường
        self.uic.input_attendance_face_school.setText(data_detect[3])

    # Hàm mở thư mục điểm danh khuôn mặt
    def open_folder_excel_face(self):
        import webbrowser
        path = "https://docs.google.com/spreadsheets/d/1Zb8mKW9TAwOIAJXyXopS_ldpPcStT7G6Zno0SOJm2QI/edit#gid=2044441802"
        webbrowser.open(path)

    # Cập nhật dữ liệu
    #     def update_data_face(self):
    #         thoigian = datetime.datetime.now()
    #         ngay = thoigian.day
    #         thang = thoigian.month
    #         nam = thoigian.year
    #         f = open("time_update/thoigian.txt", mode="w+", encoding="utf-8-sig")
    #         f.write(f"{ngay}-{thang}-{nam}")
    #         f.close()
    #         path = "dataset"
    #         recognizer = cv2.face.LBPHFaceRecognizer_create()
    #         # LBHFaceRecognizer_create()
    #         detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    #
    #         # Hàm lấy nhãn
    #         def getImagesAndLabels(path):
    #             imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    #             faceSamples = []
    #             ids = []
    #
    #             for imagePaths in imagePaths:
    #                 PIL_img = Image.open(imagePaths).convert("L")
    #                 img_numpy = np.array(PIL_img, "uint8")
    #                 id = int(os.path.split(imagePaths)[-1].split(".")[1])
    #                 faces = detector.detectMultiScale(img_numpy)
    #
    #                 for (x, y, w, h) in faces:
    #                     faceSamples.append(img_numpy[y:y + h, x: x + w])
    #                     ids.append(id)
    #             return faceSamples, ids
    #
    #         print("Đang train dữ liệu...")
    #     faces, ids = getImagesAndLabels(path)
    #     recognizer.train(faces, np.array(ids))
    #
    #     recognizer.write("trainer.yml")
    #     # Ghi lại thời gian
    #     f = open("time_update/thoigian.txt", mode="r", encoding="utf-8-sig")
    #     time_update = f.readline().strip()
    #     print("Đã train xong".format(len(np.unique(ids))))
    #     self.uic.time_data_update.setText(f"Lần cập nhật gần nhất vào ngày: {time_update}")
    #     self.uic.label_tinh_trang.setText("Tình trạng: Đã cập nhật dữ liệu")

            # Nút từ màn hình menu điểm danh bằng qr sang điểm danh bằng mã qr

    def qt_display_attendance_qr(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_attendace)

            # Nút từ màn hình menu điểm danh qua màn hình điểm danh bằng mã qr

    def qt_diplay_attendance_qr(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_attendance_qr_code)

            # Nút từ màn hình điểm danh bằng mã QR vào màn hình tạo mã QR

    def qt_display_make_data_qr(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_data)

            # Trở về màn hình menu

    def qt_display_menu(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_menu)

    def qt_display_detec(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_detec)
    def qt_display_attendance(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_diem_danh_menu)

            # Từ menu sang màn hình QR

    def qt_display_qr(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_data)

            # Tu Menu sang màn hình tự luận

    def qt_display_tu_luan(self):
        self.uic.main_widget.setCurrentWidget(self.uic.display_tuluan)
            # Hàm chạy camera

    def start_detect(self):
    # self.thread = {}
        # Bật lại nút hoàn thành
        self.uic.btn_detec_finish.setEnabled(True)
            # Tắt nút xoá

            # Tắt nút chọn môn
        self.uic.btn_select_subject.setEnabled(False)


        #Vô hiệu hoá nút bắt đầu
        self.uic.btn_detec_start.setEnabled(False)
        #Vô hiệu hoá nút qua bot email
        self.uic.btn_detec_bot_telegram.setEnabled(False)
        # Vô hiệu hoá nút trở về
        self.uic.btn_detect_menu_return.setEnabled(False)
        # Khoá tất cả các nút lại
        # Khoá nút tên
        self.uic.input_cam.setEnabled(False)
        self.uic.input_detec_name.setEnabled(False)
        # Khoá nút số báo danh
        self.uic.input_detec_sbd.setEnabled(False)
        # Khoá nút tên trường
        self.uic.input_detec_school.setEnabled(False)
        # Khoá nút tên lớp
        self.uic.input_detec_class.setEnabled(False)
        #Khoá nút môn
        self.uic.input_detec_subject.setEnabled(False)
        chay = open("Kiem_tra_luong_chay/kiem_tra.txt", "w+")
        chay.write("chay")
        chay.close()
        idx = 0
        try:
            idx = int(self.uic.input_cam.text())
            print(idx)
        except:
            print("Chỉ số cam phải là số nguyên, chuyển về cam 0")
            pass
        self.thread[1] = live_stream(index=idx)
        self.thread[1].start()
        self.thread[1].signal_khoi_dong_audio.connect(self.khoi_dong_audio)
        # Kết nối với tín hiệu
        self.thread[1].signal.connect(self.show_wedcam)
        #Kết nối với việc thông báo dữ liệu
        self.thread[1].signal_thong_bao.connect(self.show_thong_bao)
        #Khởi động audio
        print("Bắt đầu gửi tín hiệu để khởi động audio")
        self.thread[1].signal_ngung.connect(self.tam_dung_audio)
        # #Kết thúc chương trình audio
        self.thread[1].signal_ket_thuc_audio.connect(self.ket_thuc_audio)





        print("Truyền luồng")
        # Nếu có dữ liệu rồi thi moi thuc hien ghi bai
        noidung = self.uic.input_detec_name.text()
        if noidung != "":
            # Ghi nội dung file google sheets
            import datetime
            import gspread
            from xoa_tieng_viet import no_accent_vietnamese
            gs = gspread.service_account("token_gen_10012023.json")  # Truyền nguồn dữ liệu
            # sht = gs.open_by_key("1NfVvEe3zvqQf_E0WJKPzOjXFLMwaeLGSVoJztPdmjV0")
            sht = gs.open_by_key("1Zb8mKW9TAwOIAJXyXopS_ldpPcStT7G6Zno0SOJm2QI")
            #Mẫu link dự phòng đang test
            # gs = gspread.service_account("key_du_phong_hoc_sinh.json")
            # sht = gs.open_by_key("1c_QPw7y1lqDFe9bp1bzMmU53p56UeW1utzFKcz3OIzs")
            print(sht.title)  # In tiêu đề ra
            worksheet = sht.get_worksheet(0)  # Truy cập vào sheets lịch sử làm bài
            # Kiểm tra xem trong file có nội dung không
            col_test = worksheet.col_values(1)  # Lấy giá trị dòng
            # Nếu mảng trống thì ghi tiêu đề vào
            if len(col_test) == 0:
                tieu_de = ["Tên học sinh", "Số báo danh", "Tên trường", "Phòng thi", "Thời gian", "Ngày/Tháng/Năm",
                           "Nội dung","Môn Thi"]
                so_tieu_de = ["A1", "B1", "C1", "D1", "E1", "F1", "G1","H1"]
                # Ghi tiêu đề vào file
                for i in range(8):
                    worksheet.update_acell(so_tieu_de[i], tieu_de[i])  # Ghi file
                    worksheet.format("A1:H1", {
                        "horizontalAlignment": "CENTER",
                        "textFormat": {
                            "fontSize": 13,
                            "bold": True
                        }
                    })
            else:
                pass
            worksheet.format("A2:H80", {"horizontalAlignment": "CENTER", "textFormat": {"fontSize": 13, }})
            col_test = worksheet.col_values(1)  # Lấy giá trị dòng
            # Truy cập vào dòng khả thi
            row_empty = len(col_test) + 1
            index_content = ["A", "B", "C", "D", "E", "F", "G","H"]
            print("Dòng khả thi:", row_empty)
            # Khai báo mảng thông tin
            mang_thong_tin = []
            # Lấy content
            # Lấy tên
            name = self.uic.input_detec_name.text()
            # Lấy số báo danh
            sbd = self.uic.input_detec_sbd.text()
            # Lấy tên trường
            schools = self.uic.input_detec_school.text()
            # Lấy tên lớp
            class_name = self.uic.input_detec_class.text()
            #Lấy môn thi
            subject = self.uic.input_detec_subject.text()
            # Lấy thời gian hiện tại
            thoi_gian = datetime.datetime.now()
            # Lấy giờ
            gio = thoi_gian.hour
            # Lấy phút
            phut = thoi_gian.minute
            # Lấy giây
            giay = thoi_gian.second
            # Lấy ngày
            ngay = thoi_gian.day
            # Lấy tháng
            thang = thoi_gian.month
            # Lấy năm
            nam = thoi_gian.year
            thoi_gian_lam_bai = f"{gio}:{phut}:{giay}"
            vao_luc = f"{ngay}/{thang}/{nam}"
            # Thêm nội dung vào mảng vừa tạo
            # Thêm tên
            mang_thong_tin.append(name)
            # Thêm số báo danh
            mang_thong_tin.append(sbd)
            # Thêm tên trường
            mang_thong_tin.append(schools)
            # Thêm lớp
            mang_thong_tin.append(class_name)
            # Thêm thời gian vào làm bài
            mang_thong_tin.append(thoi_gian_lam_bai)
            # Thêm ngày tháng làm bài
            mang_thong_tin.append(vao_luc)
            loaihinh = "Bắt đầu làm bài"
            # Thêm nội dung vào mảng
            mang_thong_tin.append(loaihinh)
            #Thêm môn thi vào mảng
            mang_thong_tin.append(subject)
            #Thêm môn thi vào mảng
            for i in range(8):
                so_chi_muc = f"{index_content[i]}{row_empty}"
                worksheet.update_acell(so_chi_muc, str(mang_thong_tin[i]))
        else:
            pass
        self.uic.trang_thai.setText("Trạng thái: Đang làm bài")

    #Khởi động giám sát âm thanh
    def khoi_dong_audio(self, gt):
        print("Khởi động audio")
        if gt == "Bat":
            self.thread[9] = detect_audio(index = 9)
            self.thread[9].start()
            self.thread[9].signal_giam_sat.connect(self.dung_giam_sat)
            self.thread[9].signal_thong_bao_am_thanh.connect(self.show_thong_bao_am_thanh)



    #Hàm thông báo âm thanh
    def show_thong_bao_am_thanh(self,so):
        if so == 1:
            #QMessageBox.information(self, "Nhắc nhở vi phạm", "Thí sinh vui lòng giữ trật tự (Lần 1)")
            QMessageBox.information(self, "Nhắc nhở vi phạm", "Thí sinh vui lòng giữ trật tự (Lần 1)")
        elif so == 2:
            #QMessageBox.information(self, "Nhắc nhở vi phạm", "Thí sinh vui lòng giữ trật tự (Lần 2)")
            QMessageBox.information(self, "Nhắc nhở vi phạm", "Thí sinh vui lòng giữ trật tự (Lần 2)")
        elif so == 3:
            QMessageBox.information(self, "AI Xác Nhận Bạn Đã Vi Phạm Quy Chế Thi!")

    #Dừng giám sát
    def dung_giam_sat(self):
        self.thread[1].stop()
    #Kết thúc audio
    def ket_thuc_audio(self,gt):
        print("Hàm kết thúc audio")
        if gt == "Dung":
            self.thread[9].stop()
        else:
            print("Bỏ qua")
    #Hàm giám sát âm thanh
    def giam_sat_am_thanh(self, a):
        name = a
        print("Tên của bạn là:",name)


    # Hàm chạy điểm danh qua mã QR
    def start_qr(self):
        self.thread[2] = Attendance_qr_class(index=2)
        self.thread[2].start()
        # Kết nối với tín hiệu
        self.thread[2].signal1.connect(self.show_wedcam_2)
        self.thread[2].signal2.connect(self.set_data)

    # TẠO DỮ LIỆU KHUÔN MẶT
    # def start_make_data_face(self):
    #     self.uic.label_tinh_trang.setText('Tình trạng: Chưa cập nhật')
    #     self.thread[3] = attendance_face(index=3)
    #     self.thread[3].start()
    #     # Kết nối với tính hiệu
    #     self.thread[3].signal3.connect(self.show_wedcam_attendance)

    # Hàm hiển thị webcam lên GUI
    # Giám sát
    def show_wedcam(self, cv_img):
        qt_img = convert_cv_qt(cv_img)  # Nhận dữ liệu truyền vô
        self.uic.screen_detec_camera.setPixmap(qt_img)  # Set ảnh lên màn hình

    # Điểm danh
    # Hàm hiển thị webcam lên GUI
    def show_wedcam_2(self, cv_img):
        qt_img = convert_cv_qt_attendance(cv_img)  # Nhận dữ liệu truyền vô
        self.uic.btn_attendance_camera.setPixmap(qt_img)  # Set ảnh lên màn hình

    # Tạo dữ liệu
    def show_wedcam_attendance(self, cv_img):
        qt_img = convert_cv_qt_make_data(cv_img)  # Nhận dữ liệu truyền vô
        self.uic.input_camera_make_data.setPixmap(qt_img)  # Set ảnh lên màn hình



    # Hàm ghi dữ liệu học sinh vi phạm
    def make_file_txt(self):
        #Bật lại nút bắt đầu
        self.uic.btn_detec_start.setEnabled(True)
        # Lấy dữ liệu biến name_detect
        name_detect = self.uic.input_detec_name.text()
        # Lấy dữ liệu số báo danh
        number_detect = self.uic.input_detec_sbd.text()
        # Lấy dữ liệu tên trường
        school_detect = self.uic.input_detec_school.text()
        # Lấy dữ liệu phòng thi
        class_detect = self.uic.input_detec_class.text()
        #Lấy dữ liệu môn thi
        subject_detect = self.uic.input_detec_subject.text()
        # Tạo file tên thí sinh
        f_hs = open(f"data_student/file_hs.txt", mode="w+", encoding="utf-8-sig")
        f_hs.write(f"{name_detect},{number_detect},x")
        f_hs.close()

        # Tạo file để upload
        f_hs = open(f"data_student/file_hs_upload.txt", mode="w+", encoding="utf-8-sig")
        f_hs.write(f"{name_detect},{number_detect},{school_detect},x")
        f_hs.close()
        # Ghi thông tin vào file
        f = open(f"data_student/{name_detect}_{number_detect}.txt", mode="w+", encoding="utf-8-sig")
        # Ghi nội dung
        f.write("Tên học sinh: " + str(name_detect) + "\n")
        f.write("Số báo danh: " + str(number_detect) + "\n")
        f.write("Trường: " + str(school_detect) + "\n")
        f.write("Lớp: " + str(class_detect) + "\n")
        f.write("Môn thi: " + str(subject_detect) + "\n")
        f.close()


        #Tạo file học sinh vi phạm để ghi nhận
        f_hs = open(f"data_student/file_hs_vi_pham_excel.txt", mode="w+", encoding="utf-8-sig")
        f_hs.write("Tên học sinh: " + str(name_detect) + "\n")
        f_hs.write("Số báo danh: " + str(number_detect) + "\n")
        f_hs.write("Trường: " + str(school_detect) + "\n")
        f_hs.write("Lớp: " + str(class_detect) + "\n")
        f_hs.write("Môn thi: " + str(subject_detect) + "\n")
        f_hs.close()
        #Đưa hình lên màn ảnh
        self.uic.screen_detec_camera.setPixmap(QPixmap("Image/TS_main.png"))
        self.uic.screen_detec_camera.setScaledContents(True)

        #Ghi tên trường vào file token
        ten_truong = xu_li_ten_truong(school_detect)
        f = open("Telegram_bot/schools.txt",mode = "w+",encoding="utf-8-sig")
        f.write(ten_truong)
        f.close()


        #Học sinh đang kiểm tra
        f = open("data_student/file_hoc_sinh.txt",mode = "w+",encoding="utf-8-sig")
        f.write(f"{name_detect},{number_detect},{school_detect},{class_detect},{subject_detect}")
        f.close()


    # Set dữ liệu lên màn hình điểm danh
    def set_data(self, data):
        self.uic.input_attendance_name.setText(data[0])
        self.uic.input_attendance_sdb_2.setText(data[1])
        self.uic.input_attendance_school.setText(data[2])
        self.uic.input_attendance_class.setText(data[3])

if __name__ == "__main__":
    # run app
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
