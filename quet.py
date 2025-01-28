import telegram
# Hàm gửi file học sinh vi phạm qua Telegram
def send_file_text():
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
    print("Mảng xử lí là", mang_xuli)
    name_hs = mang_xuli[0]  # Tên học sinh
    sbd_hs = mang_xuli[1]  # Số báo danh
    f.close()
    nhap = f"data_student/{name_hs}_{sbd_hs}.txt"
    # print("Tên file gửi đi là ",nhap)
    # Gửi file text
    bot.send_document(chat_id=id, document=open(f"data_student/{name_hs}_{sbd_hs}.txt", mode="r", encoding="utf-8-sig"),
                      caption="Thông tin thí sinh gian lận")



def send_photos():
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
    link_anh = "Picture/bangchung.png"
    bot.sendPhoto(chat_id=id, photo=open(link_anh, "rb"), caption='Thí sinh gian lận')


send_photos()