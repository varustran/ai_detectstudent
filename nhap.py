# infor = data_student_list
        # print("Mảng đang đọc là:",infor)
        # do_dai_mang = len(infor)
        # print("Độ dài mảng đọc được là",do_dai_mang)
        # sbd = self.uic.input_attendance_far_sbd.text()
        # print("Số báo danh đọc được là",sbd)
        # #Bước xử lí mảng
        # #Trường hợp mới chỉ nhận mã QR chưa nhận dạng được khuôn mặt
        # if (do_dai_mang == 8) and infor[1] == "" and (infor[1] != infor[5]):
        #     # mang_tam_qr = infor
        #     #Set tên
        #     self.uic.input_attendance_far_name.setText(infor[4])
        #     #Set số báo danh
        #     self.uic.input_attendance_far_sbd.setText(infor[5])
        #     #Set tên lớp
        #     self.uic.input_attendance_far_class.setText(infor[6])
        #     #Set tên trường
        #     self.uic.input_attendance_far_school.setText(infor[7])
        #     infor = []
        # #Trường hợp nhận dạng được khuôn mặt và mã QR
        # elif (do_dai_mang == 8) and (infor[1] == infor[5]):
        #     #Set tên
        #     self.uic.input_attendance_far_name.setText(infor[4])
        #     #Set số báo danh
        #     self.uic.input_attendance_far_sbd.setText(infor[5])
        #     #Set tên lớp
        #     self.uic.input_attendance_far_class.setText(infor[6])
        #     #Set tên trường
        #     self.uic.input_attendance_far_school.setText(infor[7])
        #     playsound("Audio/Dang_xac_nhan.mp3")
        #     thoi_gian = datetime.datetime.now()
        #     ngay = thoi_gian.day
        #     thang = thoi_gian.month
        #     nam = thoi_gian.year
        #     gio = thoi_gian.hour
        #     phut = thoi_gian.minute
        #     giay = thoi_gian.second
        #     thoigian = f"{gio}:{phut}:{giay}"
        #     diemdanh = "Đi trễ"
        #     ngay_thang = f"{ngay}/{thang}/{nam}"
        #     set_info_diem_danh_google_sheets_new(infor[0],infor[1],infor[3],infor[2],diemdanh,thoigian,ngay_thang)
        #     playsound("Audio/Diem_danh_thanh_cong.mp3")
        #     infor = []
        #     #Set tên
        #     self.uic.input_attendance_far_name.setText("")
        #     #Set số báo danh
        #     self.uic.input_attendance_far_sbd.setText("")
        #     #Set tên lớp
        #     self.uic.input_attendance_far_class.setText("")
        #     #Set tên trường
        #     self.uic.input_attendance_far_school.setText("")
        # #Trường hợp chỉ nhận dạng được khuôn mặt
        # elif (do_dai_mang == 5) and sbd != "" and infor[1] == sbd:
        #     playsound("Audio/Dang_xac_nhan.mp3")
        #     thoi_gian = datetime.datetime.now()
        #     ngay = thoi_gian.day
        #     thang = thoi_gian.month
        #     nam = thoi_gian.year
        #     gio = thoi_gian.hour
        #     phut = thoi_gian.minute
        #     giay = thoi_gian.second
        #     thoigian = f"{gio}:{phut}:{giay}"
        #     diemdanh = "Đi trễ"
        #     ngay_thang = f"{ngay}/{thang}/{nam}"
        #     set_info_diem_danh_google_sheets_new(infor[0],infor[1],infor[3],infor[2],diemdanh,thoigian,ngay_thang)
        #     playsound("Audio/Diem_danh_thanh_cong.mp3")
        #     infor = []
        #     #Set tên
        #     self.uic.input_attendance_far_name.setText("")
        #     #Set số báo danh
        #     self.uic.input_attendance_far_sbd.setText("")
        #     #Set tên lớp
        #     self.uic.input_attendance_far_class.setText("")
        #     #Set tên trường
        #     self.uic.input_attendance_far_school.setText("")
        # else:
        #     pass
        #
        # print("Mảng sau kiểm tra là",infor)



        # if do_dai != 0 and do_dai >= 8:
        #     name_qr = infor[4]
        #     sbd_qr = infor[5]
        #     schools_qr = infor[6]
        #     class_qr = infor[7]
        #     self.uic.input_attendance_far_name.setText(name_qr)
        #     self.uic.input_attendance_far_sbd.setText(sbd_qr)
        #     self.uic.input_attendance_far_class.setText(class_qr)
        #     self.uic.input_attendance_far_school.setText(schools_qr)
        # else:
        #     sbd_qr = ""
        # sbd = self.uic.input_attendance_far_sbd.text()
        # print("Số báo danh là",sbd)
        # if sbd != "" and name_faces != "":
        #     kt = True
        #     if sbd_faces == sbd_qr and kt == True:
        #         playsound("Audio/Dang_xac_nhan.mp3")
        #         name = self.uic.input_attendance_far_name.text()
        #         so_bao_danh = self.uic.input_attendance_far_sbd.text()
        #         lop = self.uic.input_attendance_far_class.text()
        #         truong = self.uic.input_attendance_far_school.text()
        #         print(f"{name_faces}-{sbd_faces}-{class_faces}-{school_faces}//{name}-{so_bao_danh}-{lop}-{truong}")
        #         thoi_gian = datetime.datetime.now()
        #         ngay = thoi_gian.day
        #         thang = thoi_gian.month
        #         nam = thoi_gian.year
        #         gio = thoi_gian.hour
        #         phut = thoi_gian.minute
        #         giay = thoi_gian.second
        #         thoigian = f"{gio}:{phut}:{giay}"
        #         diemdanh = "Đi trễ"
        #         ngay_thang = f"{ngay}/{thang}/{nam}"
        #         set_info_diem_danh_google_sheets_new(name,so_bao_danh,truong,lop,diemdanh,thoigian,ngay_thang)
        #         self.uic.input_attendance_far_sbd.setText("")
        #         self.uic.input_attendance_far_name.setText("")
        #         self.uic.input_attendance_far_class.setText("")
        #         self.uic.input_attendance_far_school.setText("")
        #         infor = []
        #         playsound("Audio/Diem_danh_thanh_cong.mp3")
        #         kt = False
        #         sbd = ""
        #     else:
        #         infor = []
        #
        # else:
        #     kt = False
from datetime import datetime
time = datetime.now()
print(time.hour)