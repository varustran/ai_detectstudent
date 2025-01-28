# import cv2
# import datetime as datetime
# import numpy as np
# from playsound import playsound
# from PyQt5.QtCore import QThread, pyqtSignal, Qt
# import datetime
# from xoa_tieng_viet import no_accent_vietnamese
# import gspread
# import os
# from def_important import *
from DEF_NEW import *
import tkinter as tk
from tkinter import messagebox
class Attendance_qr_class(QThread):
    signal1 = pyqtSignal(np.ndarray)
    signal2 = pyqtSignal(object)

    def __init__(self, index):
        super(Attendance_qr_class, self).__init__()
        self.device = None
        # self.out_file = None
        self.classes = None
        self.index = index
        # self.model = None
        self.gg = True
        self.player = None

    # Hàm chạy luồng
    def run(self):
        self.gg = True
        class Win:
            def popup(self,
                      title="...",
                      sentence=""):
                tk.Tk().withdraw()
                name = messagebox.showinfo(
                    title=title, message=sentence)
        os.startfile(r'cameradiemdanh.txt')
        Win().popup("Thông báo", "Vui lòng nhập số cam! Nhớ lưu lại bằng cách nhấn Ctrl + S")
        f = open("cameradiemdanh.txt", mode="r", encoding="utf-8-sig")
        a = f.readline().strip()
        if str(a) == "0" or str(a) == "1" or str(a) == "2" or str(a) == "3" or str(a) == "4" or str(a) == "5" or str(a) == "6" or str(a) == "7":
            link_cam = int(a)  # Set khi camera nhập từ phím
        else:
            link_cam = str(a)
        print(link_cam)
        cap = cv2.VideoCapture(link_cam)  # Lấy camera
        dectector = cv2.QRCodeDetector()  # Nhận dạng
        du_lieu = []
        check = True
        import datetime
        thoigian = datetime.datetime.now()
        ngay = thoigian.day
        thang = thoigian.month
        nam = thoigian.year


        while True:
            ret, frame = cap.read()
            data, one, _ = dectector.detectAndDecode(frame)
            if data:
                # print(data)
                du_lieu = data.split(",")
                print("Mảng dữ liệu là",du_lieu)
                self.signal2.emit(du_lieu)
                #playsound("Audio/quet_duoc_du_lieu.mp3")
                set_data_in_qr(data,ngay,thang,nam)
                #playsound("Audio/Diem_danh_thanh_cong.mp3")
                du_lieu = ["","","",""]
                self.signal2.emit(du_lieu)



            self.signal1.emit(frame)
            if self.gg == False:
                break
        cap.release()
        cv2.destroyAllWindows()
        self.wait()

        # if str(data) != "":
        #     a = data
        #     mang = []
        #     mang.append(a)
        #     mang_xuli = data.split(",")
        #     self.signal2.emit(mang_xuli)
        #     lop = mang_xuli[3]
        #     f_read = open(f"Excel_qr/{lop}_{ngay}_{thang}_{nam}.csv", mode="a", encoding="utf-8-sig")
        #     f_read.close()
        #     f_read = open(f"Excel_qr/{lop}_{ngay}_{thang}_{nam}.csv", mode="r", encoding="utf-8-sig")
        #     header = f_read.readline().strip()
        #     # print("Đầu dòng", header)
        #     f_read.close()
        #     if header == "":
        #         f = open(f"Excel_qr/{lop}_{ngay}_{thang}_{nam}.csv", mode="w", encoding="utf-8-sig")
        #         info = "Họ và tên, Số báo danh, Tên trường, Tên lớp, Điểm danh, Thời gian"
        #         f.write(f"{info} \n")
        #         # print("Ghi đè")
        #     else:
        #         # print("Ghi tiếp")
        #         f = open(f"Excel_qr/{lop}_{ngay}_{thang}_{nam}.csv", mode="a", encoding="utf-8-sig")
        #
        #     thoigian = datetime.datetime.now()
        #     gio = thoigian.hour
        #     phut = thoigian.minute
        #     diem_danh = ""
        #     if gio <= 6 and phut <= 45:
        #         diem_danh = " "
        #     else:
        #         diem_danh = "Đi trễ"
        #
        #     thoi_gian_now = f"{gio}:{phut}"
        #     print("Mảng xử lí tbk là:" ,mang_xuli)
        #     # print("Thông tin học sinh", mang_xuli)
        #     row = f"{mang_xuli[0]},{mang_xuli[1]},{mang_xuli[2]},{mang_xuli[3]},{diem_danh},{thoi_gian_now} \n"
        #     print(row)
        #     f.write(row)
        #     #Thêm cái ngày hiện tại vô
        #     thoi_gian = datetime.datetime.now()
        #     #Lấy ngày hiện tại
        #     ngay = thoi_gian.day
        #     #Lấy tháng hiện tại
        #     thang = thoi_gian.month
        #     #Lấy năm hiện tại
        #     nam = thoi_gian.year
        #     #Tạo thời gian
        #     ngay_thang = f"{ngay}/{thang}/{nam}"
        #     set_info_diem_danh_google_sheets(mang_xuli, diem_danh, thoi_gian_now,ngay_thang)
        # else:
        #     pass
        cap.release()
        cv2.destroyAllWindows()

    # Hàm dừng chương trình
    def stop(self):
        self.gg = False
        self.wait()
        cv2.destroyAllWindows()  # Huỷ cửa sổ Camera
        self.terminate()  # Hàm dừng luồng

    # Hàm cho điều kiện While True sai
    def pause_stream(self):
        pass
