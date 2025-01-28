import telegram  # Cài bản 13.6
# Hàm gửi ảnh qua Telegram
import mediapipe as mp
import cv2
import numpy as np
from xoa_tieng_viet import no_accent_vietnamese
def send_photos():
    #Đọc file trường
    f = open("Telegram_bot/schools.txt", mode="r",encoding="utf-8-sig")
    truong_hoc = f.readline().strip()
    f.close()
    print("Tên trường là:",truong_hoc)
    files = open(f"Telegram_bot/bot_mail_truongkhac.txt", mode = "r", encoding="utf-8-sig")
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
    bot.sendPhoto(chat_id=id, photo=open(link_anh, "rb"), caption='Thí sinh gian lận')
    bot.sendPhoto(chat_id=id, photo=open(link_anh_2, "rb"), caption='Hình ảnh AI nhận diện')


def send_photos_du_phong():
    #Đọc file trường
    f = open("Telegram_bot/schools.txt", mode="r",encoding="utf-8-sig")
    truong_hoc = f.readline().strip()
    f.close()
    print("Tên trường là:",truong_hoc)
    files = open(f"Telegram_bot/bot_mail_{truong_hoc}.txt", mode = "r", encoding="utf-8-sig")
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
    bot.sendPhoto(chat_id=id, photo=open(link_anh, "rb"), caption='Thí sinh gian lận, thông tin bên dưới')


def send_photos_giam_sat_rong():
    my_token = "6178672765:AAGj3y6PQwBjF9RDoaWJ2qkjOPuWrKOcH6Q"
    # Gọi bot
    id = "-4016753764"
    bot = telegram.Bot(token=my_token)
    link_anh = "Image/hoc_sinh_ngu.png"
    bot.sendPhoto(chat_id=id, photo=open(link_anh, "rb"), caption='Thí sinh gian lận')
def send_photos_giam_sat_ngu():
    my_token = "6178672765:AAGj3y6PQwBjF9RDoaWJ2qkjOPuWrKOcH6Q"
    # Gọi bot
    id = "-4016753764"
    bot = telegram.Bot(token=my_token)
    link_anh = "Image/hoc_sinh_rong.png"
    bot.sendPhoto(chat_id=id, photo=open(link_anh, "rb"), caption='Thí sinh ngủ')



# Hàm gửi file học sinh vi phạm qua Telegram
def send_file_text():
   #Đọc file trường
    f = open("Telegram_bot/schools.txt", mode="r",encoding="utf-8-sig")
    truong_hoc = f.readline().strip()
    f.close()
    print("Tên trường là:",truong_hoc)
    files = open(f"Telegram_bot/bot_mail_{truong_hoc}.txt", mode = "r", encoding="utf-8-sig")
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
    bot.send_document(chat_id=id, document=open(f"data_student/{name_hs}_{sbd_hs}.txt", mode="r", encoding="utf-8-sig"),
                      caption="Thông tin thí sinh gian lận")


# Khởi tạo mediapose
mp_holistic = mp.solutions.holistic
# Khởi tạo cấu trúc vẽ
mp_drawing = mp.solutions.drawing_utils


# Tạo hàm nhận dạng chuyển động
def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False  # Thiết đặt để hình ảnh này không thể ghi nữa
    results = model.process(image)  # Đưa ra dự đoán trên hình ảnh
    image.flags.writeable = True  # Thiết đặt để hình ảnh có thể ghi
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results


# Hàm vẽ lên các điểm mốc
def draw_landmarks(image, results):
    # Vẽ lên điểm nhận dạng khuôn mặt
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.POSE_CONNECTIONS)
    # Vẽ lên điểm nhận dạng cơ thể
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
    # Vẽ lên điểm nhận dạng tay trái
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    # Vẽ lên điểm nhận dạng tay phải
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)


# Vẽ kiểu cho các điểm
def draw_style_landmarks(image, results):
    # Vẽ lên điểm nhận dạng khuôn mặt
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS,
                              mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
                              mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1)
                              )
    # Vẽ lên điểm nhận dạng cơ thể
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2)
                              )
    # Vẽ lên điểm nhận dạng tay trái
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2)
                              )
    # Vẽ lên điểm nhận dạng tay phải
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                              )


# Hàm trích xuất điểm
def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in
                     results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33 * 4)
    face = np.array([[res.x, res.y, res.z] for res in
                     results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468 * 3)
    lh = np.array([[res.x, res.y, res.z] for res in
                   results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21 * 3)
    rh = np.array([[res.x, res.y, res.z] for res in
                   results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(
        21 * 3)
    return np.concatenate([pose, face, lh, rh])



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
    link_anh = r"Image/hoc_sinh_quay_cop.png"
    image = open(link_anh, "rb")
    bot.sendPhoto(chat_id=id, photo=image, caption='Hình ảnh thí sinh gian lận')
#Hàm gửi thông tin học sinh vi phạm
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
    bot.sendPhoto(chat_id=id, photo=open(link_anh, "rb"), caption='Hình ảnh thí sinh ngủ trong giờ kiểm tra')


#Hàm upload thông tin điểm danh lên google sheets
def set_info_diem_danh_google_sheets(mang_xuli, diem_danh, thoi_gian_now,ngay_thang):
    import datetime
    import gspread
    from xoa_tieng_viet import no_accent_vietnamese
    # gs = gspread.service_account("history-student.json")    #Truyền nguồn dữ liệu
    # sht = gs.open_by_key("1NfVvEe3zvqQf_E0WJKPzOjXFLMwaeLGSVoJztPdmjV0")
    gs = gspread.service_account("token_gen_10012023.json")  # Truyền nguồn dữ liệu
    # sht = gs.open_by_key("1NfVvEe3zvqQf_E0WJKPzOjXFLMwaeLGSVoJztPdmjV0")
    sht = gs.open_by_key("1Zb8mKW9TAwOIAJXyXopS_ldpPcStT7G6Zno0SOJm2QI")
    #Mẫu link dự phòng đang test
    # gs = gspread.service_account("key_du_phong_hoc_sinh.json")
    # sht = gs.open_by_key("1c_QPw7y1lqDFe9bp1bzMmU53p56UeW1utzFKcz3OIzs")
    print(sht.title) #In tiêu đề ra
    worksheet = sht.sheet1
    #Xử lí tên trường
    kiem_tra_truong = no_accent_vietnamese(mang_xuli[2])
    truong = kiem_tra_truong.lower().replace(" ","")
    truong = truong.replace(" ","")
    truong = truong.replace(" ","")
    truong = truong.replace(" ","")
    print(kiem_tra_truong)
    kiem_tra_truong = truong
    if kiem_tra_truong == "toan":
        worksheet = sht.get_worksheet(3)
    elif kiem_tra_truong == "nguvan":
        worksheet = sht.get_worksheet(4)
    elif kiem_tra_truong == "tienganh":
        worksheet = sht.get_worksheet(5)
    elif kiem_tra_truong == "khtn":
        worksheet = sht.get_worksheet(6)
    elif kiem_tra_truong == "lsdl":
        worksheet = sht.get_worksheet(7)
    elif kiem_tra_truong == "gdcd":
        worksheet = sht.get_worksheet(8)
    elif kiem_tra_truong == "tinhoc":
        worksheet = sht.get_worksheet(9)
    elif kiem_tra_truong == "hdtn":
        worksheet = sht.get_worksheet(10)
    elif kiem_tra_truong == "congnghe":
        worksheet = sht.get_worksheet(11)
    else:
        worksheet = sht.get_worksheet(2)
    #Kiểm tra xem trong file có nội dung không
    col_test = worksheet.col_values(1)  #Lấy giá trị dòng
        #Nếu mảng trống thì ghi tiêu đề vào
    if len(col_test) == 0:
                tieu_de = ["Tên học sinh","Số báo danh","Môn thi","Tên lớp","Điểm danh","Thời gian","Ngày/Tháng/Năm"]
                so_tieu_de = ["A1","B1","C1","D1","E1","F1","G1"]
                #Ghi tiêu đề vào file
                for i in range(7):
                    worksheet.update_acell(so_tieu_de[i],tieu_de[i])  #Ghi file
                worksheet.format("A1:G1", {
                        "horizontalAlignment": "CENTER",
                        "textFormat": {
                          "fontSize": 13,
                          "bold": True
                        }
                         })
    else:
        pass
    worksheet.format("A2:G80", {"horizontalAlignment": "CENTER","textFormat": {"fontSize": 13,}})
    col_test = worksheet.col_values(1)  #Lấy giá trị dòng
    #Truy cập vào dòng khả thi
    row_empty = len(col_test) + 1
    index_content = ["A","B","C","D","E","F","G"]
    print("Dòng khả thi:", row_empty)
    mang_xuli.append(diem_danh)
    mang_xuli.append(thoi_gian_now)
    for i in range(6):
        so_chi_muc = f"{index_content[i]}{row_empty}"
        if i <= 3:
            worksheet.update_acell(so_chi_muc,mang_xuli[i])
        else:
            worksheet.update_acell(so_chi_muc,mang_xuli[i])
    #Thêm cái ngày hiện tại vô
    thoi_gian = datetime.datetime.now()
    ngay = thoi_gian.day
    thang = thoi_gian.month
    nam = thoi_gian.year
    ngay_thang = f"{ngay}/{thang}/{nam}"
    ghi_ngay = f"G{row_empty}"
    worksheet.update_acell(ghi_ngay,ngay_thang)



#Hàm ghi nhận lịch sử làm bài
def history_testing(mang_xuli):
    import datetime
    import gspread
    from xoa_tieng_viet import no_accent_vietnamese
    # gs = gspread.service_account("history-student.json")    #Truyền nguồn dữ liệu
    # sht = gs.open_by_key("1NfVvEe3zvqQf_E0WJKPzOjXFLMwaeLGSVoJztPdmjV0")
    gs = gspread.service_account("token_gen_10012023.json")  # Truyền nguồn dữ liệu
    # sht = gs.open_by_key("1NfVvEe3zvqQf_E0WJKPzOjXFLMwaeLGSVoJztPdmjV0")
    sht = gs.open_by_key("1Zb8mKW9TAwOIAJXyXopS_ldpPcStT7G6Zno0SOJm2QI")
    #Mẫu link dự phòng đang test
    # gs = gspread.service_account("key_du_phong_hoc_sinh.json")
    # sht = gs.open_by_key("1c_QPw7y1lqDFe9bp1bzMmU53p56UeW1utzFKcz3OIzs")


    print(sht.title) #In tiêu đề ra
    worksheet = sht.sheet1
    #Xử lí tên trường
    kiem_tra_truong = no_accent_vietnamese(mang_xuli[2])
    truong = kiem_tra_truong.lower().replace(" ","")
    truong = truong.replace(" ","")
    truong = truong.replace(" ","")
    truong = truong.replace(" ","")
    print(kiem_tra_truong)
    kiem_tra_truong = truong

def xu_li_ten_truong(schools):
    #Xử lí tên trường
    kiem_tra_truong = no_accent_vietnamese(schools)
    truong = kiem_tra_truong.lower().replace(" ","")
    truong = truong.replace(" ","")
    truong = truong.replace(" ","")
    schools = truong.replace(" ","")
    return schools



#Ghi nhận gian lận
#Ghi nhận gian lận
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
    #Mẫu link dự phòng đang test
    # gs = gspread.service_account("key_du_phong_hoc_sinh.json")
    # sht = gs.open_by_key("1c_QPw7y1lqDFe9bp1bzMmU53p56UeW1utzFKcz3OIzs")
    print(sht.title)  # In tiêu đề ra
    worksheet = sht.get_worksheet(1)  # Truy cập vào học sinh vi phạm
    # Kiểm tra xem trong file có nội dung không
    col_test = worksheet.col_values(1)  # Lấy giá trị dòng
    # Nếu mảng trống thì ghi tiêu đề vào
    if len(col_test) == 0:
        tieu_de = ["Tên học sinh", "Số báo danh", "Tên trường", "Phòng thi", "Thời gian", "Ngày/Tháng/Năm",
                   "Nội dung vi phạm","Môn thi"]
        so_tieu_de = ["A1", "B1", "C1", "D1", "E1", "F1", "G1","H1"]
        # Ghi tiêu đề vào file
        for i in range(7):
            worksheet.update_acell(so_tieu_de[i], tieu_de[i])  # Ghi file
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
    index_content = ["A", "B", "C", "D", "E", "F", "G","H"]
    print("Dòng khả thi:", row_empty)
    # Khai báo mảng thông tin
    mang_thong_tin = []
    # Lấy content
    #Mở file học sinh
    f = open("data_student/file_hoc_sinh.txt",mode = "r",encoding="utf-8-sig")
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
    loaihinh = "Hành vi che camera giám sát"
    # Thêm nội dung vào mảng
    mang_thong_tin.append(loaihinh)
    mang_thong_tin.append(mon)
    for i in range(8):
        so_chi_muc = f"{index_content[i]}{row_empty}"
        worksheet.update_acell(so_chi_muc, mang_thong_tin[i])


#Ghi nhận nói chuyện
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
    #Mẫu link dự phòng đang test
    # gs = gspread.service_account("key_du_phong_hoc_sinh.json")
    # sht = gs.open_by_key("1c_QPw7y1lqDFe9bp1bzMmU53p56UeW1utzFKcz3OIzs")


    print(sht.title)  # In tiêu đề ra
    worksheet = sht.get_worksheet(1)  # Truy cập vào học sinh vi phạm
    # Kiểm tra xem trong file có nội dung không
    col_test = worksheet.col_values(1)  # Lấy giá trị dòng
    # Nếu mảng trống thì ghi tiêu đề vào
    if len(col_test) == 0:
        tieu_de = ["Tên học sinh", "Số báo danh", "Tên trường", "Phòng thi", "Thời gian", "Ngày/Tháng/Năm",
                   "Nội dung vi phạm","Môn thi"]
        so_tieu_de = ["A1", "B1", "C1", "D1", "E1", "F1", "G1","H1"]
        # Ghi tiêu đề vào file
        for i in range(7):
            worksheet.update_acell(so_tieu_de[i], tieu_de[i])  # Ghi file
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
    index_content = ["A", "B", "C", "D", "E", "F", "G","H"]
    print("Dòng khả thi:", row_empty)
    # Khai báo mảng thông tin
    mang_thong_tin = []
    # Lấy content
    #Mở file học sinh
    f = open("data_student/file_hoc_sinh.txt",mode = "r",encoding="utf-8-sig")
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
        worksheet.update_acell(so_chi_muc, mang_thong_tin[i])





#Hàm set thông tin cho điểm danh bằng mã qr
def set_data_in_qr(data,ngay,thang,nam):
    import datetime
    if str(data) != "":
        a = data
        mang = []
        mang.append(a)
        mang_xuli = data.split(",")
        lop = mang_xuli[3]
        f_read = open(f"Excel_qr/{lop}_{ngay}_{thang}_{nam}.csv", mode="a", encoding="utf-8-sig")
        f_read.close()
        f_read = open(f"Excel_qr/{lop}_{ngay}_{thang}_{nam}.csv", mode="r", encoding="utf-8-sig")
        header = f_read.readline().strip()
        # print("Đầu dòng", header)
        f_read.close()
        if header == "":
            f = open(f"Excel_qr/{lop}_{ngay}_{thang}_{nam}.csv", mode="w", encoding="utf-8-sig")
            info = "Họ và tên, Số báo danh, Tên trường, Tên lớp, Điểm danh, Thời gian"
            f.write(f"{info} \n")

        else:

            f = open(f"Excel_qr/{lop}_{ngay}_{thang}_{nam}.csv", mode="a", encoding="utf-8-sig")

            thoigian = datetime.datetime.now()
            gio = thoigian.hour
            phut = thoigian.minute
            diem_danh = ""
            if gio <= 6 and phut <= 45:
                diem_danh = " "
            else:
                diem_danh = "Đi trễ"

            thoi_gian_now = f"{gio}:{phut}"
            print("Mảng xử lí tbk là:" ,mang_xuli)
            # print("Thông tin học sinh", mang_xuli)
            row = f"{mang_xuli[0]},{mang_xuli[1]},{mang_xuli[2]},{mang_xuli[3]},{diem_danh},{thoi_gian_now} \n"
            print(row)
            f.write(row)
            #Thêm cái ngày hiện tại vô
            thoi_gian = datetime.datetime.now()
            #Lấy ngày hiện tại
            ngay = thoi_gian.day
            #Lấy tháng hiện tại
            thang = thoi_gian.month
            #Lấy năm hiện tại
            nam = thoi_gian.year
            #Tạo thời gian
            ngay_thang = f"{ngay}/{thang}/{nam}"
            set_info_diem_danh_google_sheets(mang_xuli, diem_danh, thoi_gian_now,ngay_thang)


#Hàm trả thời gian phút
def count_time():
    from datetime import datetime
    # Thời điểm hiện tại
    now = datetime.now()
    # Thời điểm xác định
    year = now.year
    month = now.month
    day = now.day
    gio = now.hour
    phut = now.minute

    target_time = datetime(year, month,day,gio ,phut)  # Ví dụ: 3 tháng 7, 2023 lúc 15:30
    # Đếm thời gian từ thời điểm hiện tại đến thời điểm xác định
    time_difference = target_time - now

    # Chuyển đổi thời gian sang phút
    minutes = time_difference.total_seconds() // 60

    print("Số phút từ thời điểm này đến thời điểm hiện tại là:", minutes)

def ten_tra_ve(a):
    if "THPT" in a:
        b = a.split(" ")
        b.remove("THPT")
        ten = ''
        for j in b:
            ten += j[0]
        ten = ten.upper()
    elif "THCS" in a:
        b = a.split(" ")
        b.remove("THCS")
        ten = ''
        for j in b:
            ten += j[0]
        ten = ten.upper()
    else:
        b = a.split(" ")
        ten = ""
        for j in b:
            ten += j[0]
        ten = ten.upper()
    return ten

def rut_gon_ten_bai(ten_bai):
    #Xử lí tên bài kiểm tra
    if ten_bai == "Kiểm tra thường xuyên lần 1":
        ten_bai = "TX1"
    elif ten_bai == "Kiểm tra thường xuyên lần 2":
        ten_bai = "TX2"
    elif ten_bai == "Kiểm tra thường xuyên lần 3":
        ten_bai = "TX3"
    elif ten_bai == "Kiểm tra thường xuyên lần 4":
        ten_bai = "TX4"
    elif ten_bai == "Kiểm tra thường xuyên lần 5":
        ten_bai = "TX5"
    elif ten_bai == "Kiểm tra thường xuyên lần 6":
        ten_bai = "TX6"
    elif ten_bai == "Kiểm tra thường xuyên lần 7":
        ten_bai = "TX7"
    elif ten_bai == "Kiểm tra thường xuyên lần 8":
        ten_bai = "TX8"
    elif ten_bai == "Kiểm tra thường xuyên lần 9":
        ten_bai = "TX9"
    elif ten_bai == "Kiểm tra giữa kì I":
        ten_bai = "GKI"
    elif ten_bai == "Kiểm tra giữa kì II":
        ten_bai = "GKII"
    elif ten_bai == "Kiểm tra cuối kì I":
        ten_bai = "CKI"
    elif ten_bai == "Kiểm tra cuối kì II":
        ten_bai = "CKII"
    elif ten_bai == "":
        ten_bai = "blanks"
    return ten_bai

def rut_gon_ten_truong(ten_truong):
    #Xử lí tên trường
    if ten_truong == "THPT Lê Văn Tám (LVT)":
        ten_truong = "LVT"
    elif ten_truong == "THPT Trần Văn Bảy (TVB)":
        ten_truong = "TVB"
    elif ten_truong == "THPT Mai Thanh Thế (MTT)":
        ten_truong = "MTT"
    elif ten_truong == "THCS Vĩnh Lợi (VL)":
        ten_truong = "VL"
    elif ten_truong == "THPT Nguyễn Du (ND)":
        ten_truong = "ND"
    elif ten_truong == "Trường khác (TK)":
        ten_truong = "TK"
    elif ten_truong != "":
        ten_truong = ten_tra_ve(ten_truong)
    else:
        ten_truong = ""
    return ten_truong

def rut_gon_ten_mon(ten_mon):
    #Xử lí tên môn
    if ten_mon == "Môn Toán":
        ten_mon = "toan"
    elif ten_mon == "Môn Ngữ Văn":
        ten_mon = "nguvan"
    elif ten_mon == "Môn Ngoại ngữ":
        ten_mon = "ngoaingu"
    elif ten_mon == "Môn Tin học":
        ten_mon = "tinhoc"
    elif ten_mon == "Môn Sinh học":
        ten_mon = "sinhhoc"
    elif ten_mon == "Môn Địa lí":
        ten_mon = "diali"
    elif ten_mon == "Môn Hoá học":
        ten_mon = "hoahoc"
    elif ten_mon == "Môn Lịch sử":
        ten_mon = "lichsu"
    elif ten_mon == "Môn GDCD":
        ten_mon = "gdcd"
    elif ten_mon == "Môn GDQP":
        ten_mon = "gdqp"
    elif ten_mon == "Môn Âm nhạc":
        ten_mon = "amnhac"
    elif ten_mon == "Môn Mĩ thuật":
        ten_mon = "mithuat"
    elif ten_mon == "Môn Vật lí":
        ten_mon = "vatli"
    else:
        ten_mon = "loi"
    return ten_mon



#Ghi nội dung điểm học sinh
#Thiết kế hàm ghi dữ liệu
def write_data_student_excel(ten_hoc_sinh,sbd,ten_truong_new,ten_lop_new,so_cau_dung,ten_truong,ten_mon,ten_bai,ten_mon_new,thoi_gian_nop_bai,nhan_xet):
    thong_tin_hoc_sinh = [ten_hoc_sinh,sbd,ten_truong_new,ten_lop_new,ten_bai,ten_mon_new,so_cau_dung,thoi_gian_nop_bai,nhan_xet]
    print("Mảng thông tin học sinh là",thong_tin_hoc_sinh)
    header_content = ["Tên học sinh","Số báo danh","Tên trường","Tên lớp","Tên bài kiểm tra","Tên môn","Số câu đúng","Thời gian nộp bài","Nhận xét"]
    header = ["A1","B1","C1","D1","E1","F1","G1","H1","I1"]
    keys_col = ["A","B","C","D","E","F","G","H","I"]
    #Thêm thư viện vào
    import openpyxl as op
    #Khởi tạo worksheet
    print("Tới bước đọc tên file excel")
    print(f"Thong_tin_thi_sinh/{ten_truong}_{ten_mon}_{ten_bai}.xlsx")
    wb = op.load_workbook(f"Thong_tin_thi_sinh/{ten_truong}_{ten_mon}_{ten_bai}.xlsx")
    print("Đã đọc tên file")
    #Chọn sheet
    Sheet1 = wb["Sheet"]
    #Đóng file
    wb.close()
    print("Đã đọc xong file")
    #Kiểm tra thông tin
    #Xác định cột
    column_test = "A"
    #Giá trị của cột
    column = Sheet1[column_test]
    print("Dữ liệu trong colum là",column)
    #Mảng chứa dữ liệu trong cột
    column_data = []
    #Duyệt qua từng cột
    for cell in column:
        column_data.append(cell.value)
    if column_data[0] == None:
        for i in range(9):
            Sheet1[header[i]].value = header_content[i]
        vitri = len(column_data) + 1
        for i in range(9):
            o = f"{keys_col[i]}{vitri}"
            Sheet1[o].value = thong_tin_hoc_sinh[i]
        wb.close()
        wb.save(f"Thong_tin_thi_sinh/{ten_truong}_{ten_mon}_{ten_bai}.xlsx")
    else:
        vitri = len(column_data) + 1
        for i in range(9):
            o = f"{keys_col[i]}{vitri}"
            Sheet1[o].value = thong_tin_hoc_sinh[i]
        wb.close()
        wb.save(f"Thong_tin_thi_sinh/{ten_truong}_{ten_mon}_{ten_bai}.xlsx")