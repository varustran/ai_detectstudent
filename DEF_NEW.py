import time

import telegram  # Cài bản 13.6
# Hàm gửi ảnh qua Telegram
import mediapipe as mp
import cv2
import numpy as np
from xoa_tieng_viet import no_accent_vietnamese
#import cv2
#from gaze_tracking import GazeTracking
from class_detect_student_test import *
import asyncio


def send_photos():
    # Đọc file trường
    f = open("Telegram_bot/schools.txt", mode="r", encoding="utf-8-sig")
    truong_hoc = f.readline().strip()
    f.close()
    print("Tên trường là:", truong_hoc)
    if truong_hoc != "levantam" and truong_hoc != "tranvanbay" and truong_hoc != "maithanhthe" and truong_hoc != "vinhloi" and truong_hoc != "nguyendu":
        truong_hoc = "truongkhac"
    else:
        pass

    files = open(f"Telegram_bot/bot_mail_{truong_hoc}.txt", mode="r", encoding="utf-8-sig")
    print(f"Tên file là {truong_hoc}.txt")
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
    link_anh = "Picture/bangchung.png"
    link_anh_2 = "Picture/anh_frame.png"
    #link_anh_3 = "Picture/anh_test_mat.png"
    ok = True
    while ok :
        try:
            asyncio.run(bot.sendPhoto(chat_id=id, photo=open(link_anh, "rb"), caption='Thí sinh gian lận'))
            time.sleep(2)
            ok = False
        except:
            pass
    ok = True
    while ok:
        try:
            asyncio.run(bot.sendPhoto(chat_id=id, photo=open(link_anh_2, "rb"), caption='Hình ảnh AI nhận diện'))
            time.sleep(2)
            ok = False
        except:
            pass
    #bot.sendPhoto(chat_id=id, photo=open(link_anh_3, "rb"), caption='Hình ảnh AI nhận diện mắt')
def send_photos_che_cam():
    # Đọc file trường
    f = open("Telegram_bot/schools.txt", mode="r", encoding="utf-8-sig")
    truong_hoc = f.readline().strip()
    f.close()
    print("Tên trường là:", truong_hoc)
    if truong_hoc != "levantam" and truong_hoc != "tranvanbay" and truong_hoc != "maithanhthe" and truong_hoc != "vinhloi" and truong_hoc != "nguyendu":
        truong_hoc = "truongkhac"
    else:
        pass

    files = open(f"Telegram_bot/bot_mail_{truong_hoc}.txt", mode="r", encoding="utf-8-sig")
    print(f"Tên file là {truong_hoc}.txt")
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
    link_anh = "Picture/bangchung.png"
    # link_anh_2 = "Picture/anh_frame.png"
    #link_anh_3 = "Picture/anh_test_mat.png"
    asyncio.run(bot.sendPhoto(chat_id=id, photo=open(link_anh, "rb"), caption='Thí sinh che cam'))
    # bot.sendPhoto(chat_id=id, photo=open(link_anh_2, "rb"), caption='Hình ảnh AI nhận diện')


def send_photos_du_phong():
    # Đọc file trường
    f = open("Telegram_bot/schools.txt", mode="r", encoding="utf-8-sig")
    truong_hoc = f.readline().strip()
    f.close()
    print("Tên trường là:", truong_hoc)
    if truong_hoc != "levantam" and truong_hoc != "tranvanbay" and truong_hoc != "maithanhthe" and truong_hoc != "vinhloi" and truong_hoc != "nguyendu":
        truong_hoc = "truongkhac"
    else:
        pass

    files = open(f"Telegram_bot/bot_mail_{truong_hoc}.txt", mode="r", encoding="utf-8-sig")
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
    link_anh = "Picture/anh_du_phong.png"
    asyncio.run(bot.sendPhoto(chat_id=id, photo=open(link_anh, "rb"), caption='Thí sinh gian lận'))


def send_photos_giam_sat_rong():
    my_token = "6178672765:AAGj3y6PQwBjF9RDoaWJ2qkjOPuWrKOcH6Q"
    # Gọi bot
    id = "-4016753764"
    bot = telegram.Bot(token=my_token)
    link_anh = "Image/hoc_sinh_ngu.png"
    asyncio.run(bot.sendPhoto(chat_id=id, photo=open(link_anh, "rb"), caption='Thí sinh gian lận'))
# def send_photos_giam_sat_random():
#     my_token = "6178672765:AAGj3y6PQwBjF9RDoaWJ2qkjOPuWrKOcH6Q"
#     # Gọi bot
#     id = "-4098754906"
#     bot = telegram.Bot(token=my_token)
#     link_anh = "Image/hoc_sinh_rong.png"
#     bot.sendPhoto(chat_id=id, photo=open(link_anh, "rb"), caption='Cập nhật hình ảnh mới nhất')

# Hàm gửi file học sinh vi phạm qua Telegram
def send_file_text():
    # Đọc file trường
    f = open("Telegram_bot/schools.txt", mode="r", encoding="utf-8-sig")
    truong_hoc = f.readline().strip()
    f.close()
    print("Tên trường là:", truong_hoc)
    if truong_hoc != "levantam" and truong_hoc != "tranvanbay" and truong_hoc != "maithanhthe" and truong_hoc != "vinhloi" and truong_hoc != "nguyendu":
        truong_hoc = "truongkhac"
    else:
        pass

    files = open(f"Telegram_bot/bot_mail_{truong_hoc}.txt", mode="r", encoding="utf-8-sig")
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
    # Đọc dữ liệu tên và số báo danh
    # Đọc dữ liệu tên
    f = open(f"data_student/file_hs.txt", mode="r", encoding="utf-8-sig")
    mang = []
    info_hs = f.read()
    mang = info_hs.split(",")
    mang_xuli = []
    for i in range(2):
        dt = str(mang[i])
        dt.replace(" ", "")
        mang_xuli.append(dt)
    # print("Mảng xử lí là", mang_xuli)
    name_hs = mang_xuli[0]  # Tên học sinh
    sbd_hs = mang_xuli[1]  # Số báo danh
    f.close()
    nhap = f"data_student/{name_hs}_{sbd_hs}.txt"
    # print("Tên file gửi đi là ",nhap)
    # Gửi file text
    asyncio.run(bot.send_document(chat_id=id, document=open(f"data_student/{name_hs}_{sbd_hs}.txt", mode="r", encoding="utf-8-sig"),
                      caption="Thông tin thí sinh gian lận"))


# Hàm gửi ảnh qua Telegram
def send_photos_far_quay_cop():
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
    link_anh = "Image/hoc_sinh_quay_cop.png"
    asyncio.run(bot.sendPhoto(chat_id=id, photo=open(link_anh, "rb"), caption='Hình ảnh thí sinh gian lận'))


# Hàm gửi thông tin học sinh vi phạm
# Hàm gửi ảnh qua Telegram
def send_photos_far_sleep():
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
    link_anh = "Image/hoc_sinh_ngu.png"
    asyncio.run(bot.sendPhoto(chat_id=id, photo=open(link_anh, "rb"), caption='Hình ảnh thí sinh ngủ trong giờ kiểm tra'))


# Hàm upload thông tin điểm danh lên google sheets
def set_info_diem_danh_google_sheets(mang_xuli, diem_danh, thoi_gian_now, ngay_thang):
    import datetime
    import gspread
    from xoa_tieng_viet import no_accent_vietnamese
    # gs = gspread.service_account("history-student.json")    #Truyền nguồn dữ liệu
    # sht = gs.open_by_key("1NfVvEe3zvqQf_E0WJKPzOjXFLMwaeLGSVoJztPdmjV0")
    gs = gspread.service_account("token_gen_10012023.json")  # Truyền nguồn dữ liệu
    # sht = gs.open_by_key("1NfVvEe3zvqQf_E0WJKPzOjXFLMwaeLGSVoJztPdmjV0")
    sht = gs.open_by_key("1Zb8mKW9TAwOIAJXyXopS_ldpPcStT7G6Zno0SOJm2QI")
    # Mẫu link dự phòng đang test
    # gs = gspread.service_account("key_du_phong_hoc_sinh.json")
    # sht = gs.open_by_key("1c_QPw7y1lqDFe9bp1bzMmU53p56UeW1utzFKcz3OIzs")
    print(sht.title)  # In tiêu đề ra
    worksheet = sht.sheet1
    # Xử lí tên trường
    kiem_tra_truong = no_accent_vietnamese(mang_xuli[2])
    truong = kiem_tra_truong.lower().replace(" ", "")
    truong = truong.replace(" ", "")
    truong = truong.replace(" ", "")
    truong = truong.replace(" ", "")
    print(kiem_tra_truong)
    kiem_tra_truong = truong
    if kiem_tra_truong == "nguyentriphuong":
        worksheet = sht.get_worksheet(2)
    elif kiem_tra_truong == "nguyenchidieu":
        worksheet = sht.get_worksheet(3)
    elif kiem_tra_truong == "quochoc":
        worksheet = sht.get_worksheet(3)
    elif kiem_tra_truong == "haibatrung":
        worksheet = sht.get_worksheet(3)
    else:
        worksheet = sht.get_worksheet(6)
    # Kiểm tra xem trong file có nội dung không
    col_test = worksheet.col_values(1)  # Lấy giá trị dòng
    # Nếu mảng trống thì ghi tiêu đề vào
    if len(col_test) == 0:
        tieu_de = ["Tên học sinh", "Số báo danh", "Tên trường", "Tên lớp", "Điểm danh", "Thời gian", "Ngày/Tháng/Năm"]
        so_tieu_de = ["A1", "B1", "C1", "D1", "E1", "F1", "G1"]
        # Ghi tiêu đề vào file
        for i in range(7):
            worksheet.update(so_tieu_de[i], tieu_de[i])  # Ghi file
        worksheet.format("A1:G1", {
            "horizontalAlignment": "CENTER",
            "textFormat": {
                "fontSize": 13,
                "bold": True
            }
        })
    else:
        pass
    worksheet.format("A2:G80", {"horizontalAlignment": "CENTER", "textFormat": {"fontSize": 13, }})
    col_test = worksheet.col_values(1)  # Lấy giá trị dòng
    # Truy cập vào dòng khả thi
    row_empty = len(col_test) + 1
    index_content = ["A", "B", "C", "D", "E", "F", "G"]
    print("Dòng khả thi:", row_empty)
    mang_xuli.append(diem_danh)
    mang_xuli.append(thoi_gian_now)
    for i in range(6):
        so_chi_muc = f"{index_content[i]}{row_empty}"
        if i <= 3:
            worksheet.update(so_chi_muc, mang_xuli[i])
        else:
            worksheet.update(so_chi_muc, mang_xuli[i])
    # Thêm cái ngày hiện tại vô
    thoi_gian = datetime.datetime.now()
    ngay = thoi_gian.day
    thang = thoi_gian.month
    nam = thoi_gian.year
    ngay_thang = f"{ngay}/{thang}/{nam}"
    ghi_ngay = f"G{row_empty}"
    worksheet.update(ghi_ngay, ngay_thang)


# Hàm ghi nhận lịch sử làm bài
def history_testing(mang_xuli):
    import datetime
    import gspread
    from xoa_tieng_viet import no_accent_vietnamese
    # gs = gspread.service_account("history-student.json")    #Truyền nguồn dữ liệu
    # sht = gs.open_by_key("1NfVvEe3zvqQf_E0WJKPzOjXFLMwaeLGSVoJztPdmjV0")
    gs = gspread.service_account("token_gen_10012023.json")  # Truyền nguồn dữ liệu
    # sht = gs.open_by_key("1NfVvEe3zvqQf_E0WJKPzOjXFLMwaeLGSVoJztPdmjV0")
    sht = gs.open_by_key("1Zb8mKW9TAwOIAJXyXopS_ldpPcStT7G6Zno0SOJm2QI")
    # Mẫu link dự phòng đang test
    # gs = gspread.service_account("key_du_phong_hoc_sinh.json")
    # sht = gs.open_by_key("1c_QPw7y1lqDFe9bp1bzMmU53p56UeW1utzFKcz3OIzs")

    print(sht.title)  # In tiêu đề ra
    worksheet = sht.sheet1
    # Xử lí tên trường
    kiem_tra_truong = no_accent_vietnamese(mang_xuli[2])
    truong = kiem_tra_truong.lower().replace(" ", "")
    truong = truong.replace(" ", "")
    truong = truong.replace(" ", "")
    truong = truong.replace(" ", "")
    print(kiem_tra_truong)
    kiem_tra_truong = truong


def xu_li_ten_truong(schools):
    # Xử lí tên trường
    kiem_tra_truong = no_accent_vietnamese(schools)
    truong = kiem_tra_truong.lower().replace(" ", "")
    truong = truong.replace(" ", "")
    truong = truong.replace(" ", "")
    schools = truong.replace(" ", "")
    return schools


# Ghi nhận gian lận
# Ghi nhận gian lận
def ghi_nhan_che_cam():
    # Ghi nội dung file google sheets
    import datetime
    import gspread
    from xoa_tieng_viet import no_accent_vietnamese
    # gs = gspread.service_account("history-student.json")  # Truyền nguồn dữ liệu
    # sht = gs.open_by_key("1NfVvEe3zvqQf_E0WJKPzOjXFLMwaeLGSVoJztPdmjV0")
    gs = gspread.service_account("token_gen_10012023.json")  # Truyền nguồn dữ liệu
    # sht = gs.open_by_key("1NfVvEe3zvqQf_E0WJKPzOjXFLMwaeLGSVoJztPdmjV0")
    sht = gs.open_by_key("1Zb8mKW9TAwOIAJXyXopS_ldpPcStT7G6Zno0SOJm2QI")
    # Mẫu link dự phòng đang test
    # gs = gspread.service_account("key_du_phong_hoc_sinh.json")
    # sht = gs.open_by_key("1c_QPw7y1lqDFe9bp1bzMmU53p56UeW1utzFKcz3OIzs")
    print(sht.title)  # In tiêu đề ra
    worksheet = sht.get_worksheet(1)  # Truy cập vào học sinh vi phạm
    # Kiểm tra xem trong file có nội dung không
    col_test = worksheet.col_values(1)  # Lấy giá trị dòng
    # Nếu mảng trống thì ghi tiêu đề vào
    if len(col_test) == 0:
        tieu_de = ["Tên học sinh", "Số báo danh", "Tên trường", "Phòng thi", "Thời gian", "Ngày/Tháng/Năm",
                   "Nội dung vi phạm", "Môn thi"]
        so_tieu_de = ["A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1"]
        # Ghi tiêu đề vào file
        for i in range(7):
            worksheet.update(so_tieu_de[i], tieu_de[i])  # Ghi file
            worksheet.format("A1:G1", {
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
    index_content = ["A", "B", "C", "D", "E", "F", "G", "H"]
    print("Dòng khả thi:", row_empty)
    # Khai báo mảng thông tin
    mang_thong_tin = []
    # Lấy content
    # Mở file học sinh
    f = open("data_student/file_hoc_sinh.txt", mode="r", encoding="utf-8-sig")
    du_lieu = f.read().split(",")
    name = du_lieu[0]
    sbd = du_lieu[1]
    schools = du_lieu[2]
    class_name = du_lieu[3]
    mon = du_lieu[4]
    f.close()
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
    loaihinh = "Hành vi che camera"
    # Thêm nội dung vào mảng
    mang_thong_tin.append(loaihinh)
    mang_thong_tin.append(mon)
    for i in range(8):
        so_chi_muc = f"{index_content[i]}{row_empty}"
        worksheet.update(so_chi_muc, mang_thong_tin[i])


# Ghi nhận nói chuyện
def ghi_nhan_trao_doi():
    # Ghi nội dung file google sheets
    import datetime
    import gspread
    from xoa_tieng_viet import no_accent_vietnamese
    # gs = gspread.service_account("history-student.json")  # Truyền nguồn dữ liệu
    # sht = gs.open_by_key("1NfVvEe3zvqQf_E0WJKPzOjXFLMwaeLGSVoJztPdmjV0")
    gs = gspread.service_account("token_gen_10012023.json")  # Truyền nguồn dữ liệu
    # sht = gs.open_by_key("1NfVvEe3zvqQf_E0WJKPzOjXFLMwaeLGSVoJztPdmjV0")
    sht = gs.open_by_key("1Zb8mKW9TAwOIAJXyXopS_ldpPcStT7G6Zno0SOJm2QI")
    # Mẫu link dự phòng đang test
    # gs = gspread.service_account("key_du_phong_hoc_sinh.json")
    # sht = gs.open_by_key("1c_QPw7y1lqDFe9bp1bzMmU53p56UeW1utzFKcz3OIzs")

    print(sht.title)  # In tiêu đề ra
    worksheet = sht.get_worksheet(1)  # Truy cập vào học sinh vi phạm
    # Kiểm tra xem trong file có nội dung không
    col_test = worksheet.col_values(1)  # Lấy giá trị dòng
    # Nếu mảng trống thì ghi tiêu đề vào
    if len(col_test) == 0:
        tieu_de = ["Tên học sinh", "Số báo danh", "Tên trường", "Phòng thi", "Thời gian", "Ngày/Tháng/Năm",
                   "Nội dung vi phạm", "Môn thi"]
        so_tieu_de = ["A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1"]
        # Ghi tiêu đề vào file
        for i in range(7):
            worksheet.update(so_tieu_de[i], tieu_de[i])  # Ghi file
            worksheet.format("A1:G1", {
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
    index_content = ["A", "B", "C", "D", "E", "F", "G", "H"]
    print("Dòng khả thi:", row_empty)
    # Khai báo mảng thông tin
    mang_thong_tin = []
    # Lấy content
    # Mở file học sinh
    f = open("data_student/file_hoc_sinh.txt", mode="r", encoding="utf-8-sig")
    du_lieu = f.read().split(",")
    name = du_lieu[0]
    sbd = du_lieu[1]
    schools = du_lieu[2]
    class_name = du_lieu[3]
    mon = du_lieu[4]
    f.close()
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
    loaihinh = "Trao đổi trong giờ kiểm tra"
    # Thêm nội dung vào mảng
    mang_thong_tin.append(loaihinh)
    mang_thong_tin.append(mon)
    for i in range(8):
        so_chi_muc = f"{index_content[i]}{row_empty}"
        worksheet.update(so_chi_muc, mang_thong_tin[i])


# Hàm trả về vị trí của camera 1
def vi_tri_cam_1(frame, face_mesh, mp_face_mesh, mp_drawing, drawing_spec):
    image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)  # Chuyển đồi màu ảnh
    image.flags.writeable = False  # Gắn cờ sai
    results = face_mesh.process(image)  # Trả về kết quả nhận dạng
    image.flags.writeable = True  # Gắn cờ đúng cho ảnh
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Chuyển đổi màu ảnh
    img_h, img_w, img_c = image.shape  # Lấy kích thước hình dạng ảnh
    face_3d = []  # Tạo mảng 3 chiều
    face_2d = []  # Tạo mảng 2 chiều
    # print("Tới bước results")
    if results.multi_face_landmarks:
        # print("Đang trong results")
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
            # print("Tới bước canh toạ độ")
            if y < -28:
                text = "Trai"
                return text
            elif y > 28:
                text = "Phai"
                return text
            elif x < -20:
                text = "Dang lam bai"
                return text
            elif x > 35:
                text = "Dang ngua len"
                return text
            else:
                text = "Nhin thang"
                return text


# Hàm trả về vị trí của camera 2
def vi_tri_cam_2(frame, face_mesh, mp_face_mesh, mp_drawing, drawing_spec):
    image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)  # Chuyển đồi màu ảnh
    image.flags.writeable = False  # Gắn cờ sai
    results = face_mesh.process(image)  # Trả về kết quả nhận dạng
    image.flags.writeable = True  # Gắn cờ đúng cho ảnh
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Chuyển đổi màu ảnh
    img_h, img_w, img_c = image.shape  # Lấy kích thước hình dạng ảnh
    face_3d = []  # Tạo mảng 3 chiều
    face_2d = []  # Tạo mảng 2 chiều
    # print("Tới bước results")
    if results.multi_face_landmarks:
        # print("Đang trong results")
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
            # print("Tới bước canh toạ độ")
            if y < -28:
                text = "Trai"
                return text
            elif y > 28:
                text = "Phai"
                return text
            elif x < -35:
                text = "Dang lam bai"
                return text
            elif x > 35:
                text = "Dang ngua len"
                return text
            else:
                text = "Nhin thang"
                return text


# Hàm xử lí ảnh cho giám sát rộng
def xu_li_anh(frame, face_mesh, mp_face_mesh, mp_drawing, drawing_spec):
    image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)  # Chuyển đồi màu ảnh
    image.flags.writeable = False  # Gắn cờ sai
    results = face_mesh.process(image)  # Trả về kết quả nhận dạng
    image.flags.writeable = True  # Gắn cờ đúng cho ảnh
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Chuyển đổi màu ảnh
    img_h, img_w, img_c = image.shape  # Lấy kích thước hình dạng ảnh
    face_3d = []  # Tạo mảng 3 chiều
    face_2d = []  # Tạo mảng 2 chiều
    # print("Tới bước results")
    if results.multi_face_landmarks:
        # print("Đang trong results")
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
            # print("Tới bước canh toạ độ")
            if y < -28:
                text = "Trai"
                # self.kiemtra.append(1)
                # f = open("Condition/camera_phai.txt",mode = "w",encoding="utf-8-sig")
                # f.write("Trai")
                # f.close()
            elif y > 28:
                text = "Phai"
                # f = open("Condition/camera_phai.txt",mode = "w",encoding="utf-8-sig")
                # f.write("Phai")
                # f.close()
                # self.kiemtra.append(1)
            elif x < -35:
                text = "Dang lam bai"

            elif x > 35:
                text = "Dang ngua len"

            else:
                text = "Nhin thang"

            nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix,
                                                             dist_matrix)
            p1 = (int(nose_2d[0]), int(nose_2d[1]))
            p2 = (int(nose_2d[0] + y * 10), int(nose_2d[1] - x * 10))
            cv2.line(image, p1, p2, (255, 0, 0), 3)
            cv2.circle(image, p1, 10, (0, 0, 255), -1)
            cv2.circle(image, p2, 10, (0, 0, 255), -1)
            cv2.putText(image, text, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec)
            # print("Truyền tín hiệu đi rồi")
    return image


# Hàm xử lí ảnh giám sát rộng
def xu_li_anh_2(frame, face_mesh, mp_face_mesh, mp_drawing, drawing_spec):
    image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)  # Chuyển đồi màu ảnh
    image.flags.writeable = False  # Gắn cờ sai
    results = face_mesh.process(image)  # Trả về kết quả nhận dạng
    image.flags.writeable = True  # Gắn cờ đúng cho ảnh
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Chuyển đổi màu ảnh
    img_h, img_w, img_c = image.shape  # Lấy kích thước hình dạng ảnh
    face_3d = []  # Tạo mảng 3 chiều
    face_2d = []  # Tạo mảng 2 chiều
    # print("Tới bước results")
    if results.multi_face_landmarks:
        # print("Đang trong results")
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
            # print("Tới bước canh toạ độ")
            if y < -30:
                text = "Trai"
                # self.kiemtra.append(1)
            elif y > 30:
                text = "Phai"
                # (1)
            elif x < -30:
                text = "Dang lam bai"
            elif x > 30:
                text = "Dang ngua len"
            else:
                text = "Nhin thang"
            nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix,
                                                             dist_matrix)
            p1 = (int(nose_2d[0]), int(nose_2d[1]))
            p2 = (int(nose_2d[0] + y * 10), int(nose_2d[1] - x * 10))
            cv2.line(image, p1, p2, (255, 0, 0), 3)
            cv2.circle(image, p1, 10, (0, 0, 255), -1)
            cv2.circle(image, p2, 10, (0, 0, 255), -1)
            cv2.putText(image, text, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec)
            # print("Truyền tín hiệu đi rồi")
    return image


# Hàm gửi ảnh qua Telegram
def send_photos_far_2_cam(link_anh, cap):
    my_token = "6178672765:AAGj3y6PQwBjF9RDoaWJ2qkjOPuWrKOcH6Q"
    id = "-4057529611"
    # Gọi bot
    bot = telegram.Bot(token=my_token)
    link_anh = f"Image_student/{link_anh}"
    asyncio.run(bot.sendPhoto(chat_id=id, photo=open(link_anh, "rb"), caption=f'{cap}'))


# Tạo mã qr và gửi chúng đi
def make_qr_send(name, sbd, truong, lop):
    # Thêm thư viện qr code
    import qrcode
    from PIL import Image
    qr = qrcode.QRCode(version=5, error_correction=qrcode.ERROR_CORRECT_M,
                       box_size=5, border=3)
    name = name
    sbd = sbd
    school = truong
    class_hs = lop
    truong = xu_li_ten_truong(school)
    f = open("Telegram_bot/schools.txt", mode="w", encoding="utf-8-sig")
    f.write(f"{truong}")
    f.close()
    # Thêm dữ liệu vào qr_code
    qr.add_data(f"{name},{sbd},{school},{class_hs}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("QR_code.png")
    # khởi tạo link ảnh
    link_anh = f"MA_QR/{name}_{sbd}_{school}_{class_hs}.png"
    img.save(link_anh)
    import telegram
    # Đọc file trường
    f = open("Telegram_bot/schools.txt", mode="r", encoding="utf-8-sig")
    truong_hoc = f.readline().strip()
    f.close()
    if truong_hoc != "levantam" and truong_hoc != "tranvanbay" and truong_hoc and "maithanhthe" and truong_hoc != "vinhloi" and truong_hoc != "nguyendu":
        truong_hoc = "truongkhac"
    else:
        pass

    print("Tên trường là:", truong_hoc)
    files = open(f"Telegram_bot/bot_qr_{truong_hoc}.txt", mode="r", encoding="utf-8-sig")
    mang = []
    a = files.read()
    mang = a.split(",")
    mang_xuli = []
    for i in range(2):
        dt = str(mang[i])
        dt.replace(" ", "")
        mang_xuli.append(dt)
    my_token = mang_xuli[0]  # ID
    id = mang_xuli[1]  # Token
    print("My token là", my_token)
    print("ID là", id)
    # Gọi bot
    bot = telegram.Bot(token=my_token)
    asyncio.run(bot.send_photo(chat_id=id, photo=open("QR_code.png", "rb"), caption="Thông tin học sinh QR-CODE\n"
                                                                        f"Tên học sinh: {name}\n"
                                                                        f"Số báo danh: {sbd}\n"
                                                                        f"Tên trường: {school}\n"
                                                                        f"Tên lớp: {class_hs}"))


# Hàm xử lí khuôn mặt



# Hàm lấy số báo danh của khuôn mặt
# def load_faces_numbers(frame, names, minW, minH, recognizer, faceCascade):
#     # Hàm xử lí khuôn mặt
#     # print("Tới bước đọc ảnh")
#     img = cv2.flip(frame, 1)
#     # print("Đã đọc được ảnh")
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(int(minW), int(minH)))
#     # print("Tới vòng lặp for")
#     for (x, y, w, h) in faces:
#         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         id, confidence = recognizer.predict(gray[y:y + h, x: w + x])
#         # print("Loại confidence là",type(confidence))
#         if (confidence < 100):
#             id = names[id]
#             confidence = "  {0}%".format(round(100 - confidence))
#             name = confidence
#             # print("Tên là",id)
#             return id
#         else:
#             id = "Chua xac dinh"
#             # print("Tới bước trả id")
#             return id

#
# def send_photos_mat():
#     #Đọc file trường
#     f = open("Telegram_bot/schools.txt", mode="r",encoding="utf-8-sig")
#     truong_hoc = f.readline().strip()
#     f.close()
#     #print("Tên trường là:",truong_hoc)
#     files = open(f"Telegram_bot/bot_mail_truongkhac.txt", mode = "r", encoding="utf-8-sig")
#     mang = []
#     a = files.read()
#     mang = a.split(",")
#     mang_xuli = []
#     for i in range(2):
#         dt = str(mang[i])
#         dt.replace(" ", "")
#         mang_xuli.append(dt)
#     my_token = mang[0]  # ID
#     id = mang[1]  # Token
#     # Gọi bot
#     bot = telegram.Bot(token=my_token)
#     link_anh = "Picture/anh_test_mat.png"
#     bot.sendPhoto(chat_id=id, photo=open(link_anh, "rb"), caption='Hình ảnh AI nhận diện mắt')
# Hàm lấy số báo danh học sinh
def load_numbers():
    # Mở file chứa thông tin học sinh ra
    f = open("info_student/model.csv", mode="r", encoding="utf-8-sig")
    # Đọc dòng thứ 1 của file
    header = f.readline().strip()
    # Tạo mảng chưa data học sinh
    data_so_bao_danh = []
    # Đọc dòng thứ 2
    row = f.readline().strip()
    # Nếu dòng thứ 2 khác rỗng thì
    while row != "":
        data_so_bao_danh.append(row)  # Thêm dòng hiện hành vào mảng data học sinh
        row = f.readline().strip()  # Đọc dòng tiếp theo để kiểm tra
    # Khởi tạo mảng số báo danh
    mang_sbd = []
    f.close()
    # Dùng vòng lặp for để xử lí tên
    for i in data_so_bao_danh:
        mang_tam = i.split(",")
        # print(mang_tam)
        mang_sbd.append(mang_tam[2])
    return mang_sbd


# Hàm thêm dữ liệu vào mảng
def return_data_in_list(so_bao_danh):
    # Mở file chứa thông tin học sinh ra
    f = open("info_student/model.csv", mode="r", encoding="utf-8-sig")
    # Đọc dòng thứ 1 của file
    header = f.readline().strip()
    # Tạo mảng chưa data học sinh
    data_so_bao_danh = []
    # Đọc dòng thứ 2
    row = f.readline().strip()
    # Nếu dòng thứ 2 khác rỗng thì
    while row != "":
        data_so_bao_danh.append(row)  # Thêm dòng hiện hành vào mảng data học sinh
        row = f.readline().strip()  # Đọc dòng tiếp theo để kiểm tra
    # Khởi tạo mảng số báo danh
    f.close()
    # Tạo mảng data
    mang_data = []
    # Khai báo biến tên
    name = ""
    # Khai báo số báo danh
    sbd = ""
    # Khai báo lớp
    lop = ""
    # Khai báo trường
    truong = ""
    if so_bao_danh != None:
        for i in data_so_bao_danh:
            mang_tam = i.split(",")
            for j in range(len(mang_tam)):
                if mang_tam[j] == so_bao_danh:
                    name = mang_tam[1]
                    sbd = mang_tam[2]
                    lop = mang_tam[3]
                    truong = mang_tam[4]
    print(f"Hàm trả về kết quả của mảng là {name}-{sbd}-{lop}-{truong}")
    # Thêm tên vào mảng dữ liệu
    mang_data.append(name)
    # Them báo danh vào mảng dữ liệu
    mang_data.append(sbd)
    # Thêm lớp vào mảng dữ liệu
    mang_data.append(lop)
    # Thêm tên trường vào mảng dữ liệu
    mang_data.append(truong)
    return mang_data


# Lấy thông tin từ mã qr
def return_list_qr_data(frame, detector):
    qr_not_found_count = 0
    data, _, _ = detector.detectAndDecode(frame)
    if data:
        a = data.split(",")
        print("Dữ liệu trong mảng QR là", a)
        qr_not_found_count = 0
        return data
    else:
        qr_not_found_count += 1
        if qr_not_found_count > 10:  # Số lần không tìm thấy mã QR vượt quá ngưỡng
            print("Không nhìn thấy mã QR trong một khoảng thời gian dài")
            # Thực hiện hành động của bạn ở đây
        return []


# Hàm điểm danh của điểm danh diện rộng
def set_info_diem_danh_google_sheets_new(name, sbd, schools, lop, diemdanh, thoigian, date):
    import datetime
    import gspread
    from xoa_tieng_viet import no_accent_vietnamese
    # gs = gspread.service_account("history-student.json")    #Truyền nguồn dữ liệu
    # sht = gs.open_by_key("1NfVvEe3zvqQf_E0WJKPzOjXFLMwaeLGSVoJztPdmjV0")
    gs = gspread.service_account("token_gen_10012023.json")  # Truyền nguồn dữ liệu
    # sht = gs.open_by_key("1NfVvEe3zvqQf_E0WJKPzOjXFLMwaeLGSVoJztPdmjV0")
    sht = gs.open_by_key("1Zb8mKW9TAwOIAJXyXopS_ldpPcStT7G6Zno0SOJm2QI")
    # Mẫu link dự phòng đang test
    # gs = gspread.service_account("key_du_phong_hoc_sinh.json")
    # sht = gs.open_by_key("1c_QPw7y1lqDFe9bp1bzMmU53p56UeW1utzFKcz3OIzs")
    print(sht.title)  # In tiêu đề ra
    worksheet = sht.sheet1
    # Xử lí tên trường
    kiem_tra_truong = no_accent_vietnamese(schools)
    truong = kiem_tra_truong.lower().replace(" ", "")
    truong = truong.replace(" ", "")
    truong = truong.replace(" ", "")
    truong = truong.replace(" ", "")
    print("Trường đã xử lí", truong)
    kiem_tra_truong = truong
    if kiem_tra_truong == "tienganh":
        worksheet = sht.get_worksheet(2)
    elif kiem_tra_truong == "toan":
        worksheet = sht.get_worksheet(2)
    elif kiem_tra_truong == "vinhloi":
        worksheet = sht.get_worksheet(3)
    elif kiem_tra_truong == "maithanhthe":
        worksheet = sht.get_worksheet(3)  # Trường mai thanh thế
    elif kiem_tra_truong == "ntp":
        worksheet = sht.get_worksheet(2)
    elif kiem_tra_truong == "nguyentriphuong":
        worksheet = sht.get_worksheet(2)
    else:
        worksheet = sht.get_worksheet(2)
    # Kiểm tra xem trong file có nội dung không
    col_test = worksheet.col_values(1)
    # Nếu mảng trống thì ghi tiêu đề vào
    if len(col_test) == 0:
        tieu_de = ["Tên học sinh", "Số báo danh", "Môn thi", "Tên lớp", "Điểm danh", "Thời gian", "Ngày/Tháng/Năm"]
        so_tieu_de = ["A1", "B1", "C1", "D1", "E1", "F1", "G1"]
        # Ghi tiêu đề vào file
        for i in range(7):
            worksheet.update(so_tieu_de[i], tieu_de[i])  # Ghi file
        worksheet.format("A1:G1", {
            "horizontalAlignment": "CENTER",
            "textFormat": {
                "fontSize": 13,
                "bold": True
            }
        })
    else:
        pass
    worksheet.format("A2:G80", {"horizontalAlignment": "CENTER", "textFormat": {"fontSize": 13, }})
    col_test = worksheet.col_values(1)  # Lấy giá trị dòng
    # Truy cập vào dòng khả thi
    row_empty = len(col_test) + 1
    index_content = ["A", "B", "C", "D", "E", "F", "G"]
    print("Dòng khả thi:", row_empty)
    mang_xuli = []
    mang_xuli.append(name)
    mang_xuli.append(sbd)
    mang_xuli.append(schools)
    mang_xuli.append(lop)
    mang_xuli.append(diemdanh)
    mang_xuli.append(thoigian)
    mang_xuli.append(date)
    for i in range(7):
        so_chi_muc = f"{index_content[i]}{row_empty}"
        worksheet.update(so_chi_muc, mang_xuli[i])

    # #Thêm cái ngày hiện tại vô


# name = "lê trần ngọc hiếu"
# sbd = "123"
# truong = "THCS Nguyễn Tri Phương"
# lop = "8/1"
# make_qr_send(name,sbd,truong,lop)


def make_qr_send_telegram(name, sbd, truong, lop):
    # Thêm thư viện qr code
    import qrcode
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
    qr = qrcode.QRCode(version=5, error_correction=qrcode.ERROR_CORRECT_M,
                       box_size=5, border=3)
    name = name
    sbd = sbd
    school = truong
    class_hs = lop
    truong = xu_li_ten_truong(school)
    f = open("Telegram_bot/schools.txt", mode="w", encoding="utf-8-sig")
    f.write(f"{truong}")
    f.close()
    # Thêm dữ liệu vào qr_code
    qr.add_data(f"{name},{sbd},{school},{class_hs}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("QR_code.png")
    # khởi tạo link ảnh
    # link_anh = f"MA_QR/{name}_{sbd}_{school}_{class_hs}.png"
    # img.save(link_anh)
    import telegram
    # Đọc file trường
    f = open("Telegram_bot/schools.txt", mode="r", encoding="utf-8-sig")
    truong_hoc = f.readline().strip()
    f.close()
    if truong_hoc != "levantam" and truong_hoc != "tranvanbay" and truong_hoc != "maithanhthe" and truong_hoc != "vinhloi" and truong_hoc != "nguyendu":
        truong_hoc = "truongkhac"
    else:
        pass
    print("Tên trường là:", truong_hoc)
    files = open(f"Telegram_bot/bot_qr_{truong_hoc}.txt", mode="r", encoding="utf-8-sig")
    mang = []
    a = files.read()
    mang = a.split(",")
    mang_xuli = []
    for i in range(2):
        dt = str(mang[i])
        dt.replace(" ", "")
        mang_xuli.append(dt)
    my_token = mang_xuli[0]  # ID
    id = mang_xuli[1]  # Token
    print("My token là", my_token)
    print("ID là", id)
    # Gọi bot
    bot = telegram.Bot(token=my_token)
    asyncio.run(bot.send_photo(chat_id=id, photo=open("QR_code.png", "rb"), caption="Thông tin học sinh QR-CODE\n"
                                                                        f"Tên học sinh: {name}\n"
                                                                        f"Số báo danh: {sbd}\n"
                                                                        f"Môn thi: {school}\n"

                                                                        f"Tên lớp: {class_hs}"))

import speech_recognition


# Khởi động micro
def start_micro():
    ai_brain = " "  # Ban đầu nó chưa được học gì cả nên cũng chưa có thông tin
    ai_ear = speech_recognition.Recognizer()  # nghe người dùng nói
    you = ""  # Lời nói người dùng
    # print("Khởi động mic")
    with speech_recognition.Microphone() as mic:
        # print("Đang test mic")
        audio = ai_ear.record(mic, duration=3)


# Hàm điểm danh
def diem_danh_hoc_sinh(ten, sbd, truong, lop):
    from datetime import datetime
    thoi_gian = datetime.now()
    ngay = thoi_gian.day
    thang = thoi_gian.month
    nam = thoi_gian.year
    gio = thoi_gian.hour
    phut = thoi_gian.minute
    giay = thoi_gian.second
    thoigian = f"{gio}:{phut}:{giay}"
    buoi = ""
    if gio <= 12:
        buoi = "morning"
    else:
        buoi = "afternoon"

    print("Buổi là", buoi)
    truong_xl = xu_li_ten_truong(truong)
    f = open(f"Time_setup/{truong_xl}_{lop}_{buoi}.txt", mode="r", encoding="utf-8-sig")
    tg = f.readline().split(",")
    print("Thời gian là", tg)
    f.close()
    gio_thoi_gian = int(tg[0])
    phut_thoi_gian = int(tg[1])
    print(f"Giờ điểm danh là:{gio}:{phut}")
    print(type(gio))
    if gio > 1 and gio < 12:
        # Buổi sáng
        if gio < gio_thoi_gian:
            diem_danh = "Đúng giờ"
        elif gio == gio_thoi_gian and phut <= phut_thoi_gian:
            diem_danh = "Đúng giờ"
        else:
            diem_danh = "Đi trễ"
    else:
        if gio < gio_thoi_gian:
            diem_danh = "Đúng giờ"
        elif gio == gio_thoi_gian and phut <= phut_thoi_gian:
            diem_danh = "Đúng giờ"
        else:
            diem_danh = "Đi trễ"
    print("Vào thi:", diem_danh)
    thoi_gian = f"{gio}:{phut}:{giay}"
    ngay_thang = f"{ngay}/{thang}/{nam}"
    set_info_diem_danh_google_sheets_new(ten, sbd, truong, lop, diem_danh, thoi_gian, ngay_thang)

