from quickstart import google_drive_API

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

def upload_image_qr(link_image,link_up):
    #UPDATE DATA
    service = google_drive_API()
    #Khởi tạo ID của thư mục
    folder_id_hs_vp = ["1dvBvfjXIZL3MxFWRE6_nGZCkVbx81bZD"]
    #Khởi tạo file học sinh
    name_link = []
    link = link_image
    name_link.append(link)
    file_name = name_link
    #Khởi tạo cấu trúc body
    file_metadata = {
        "name": file_name,
        "parents": folder_id_hs_vp
    }
    #Khởi tạo đường dẫn MEDIA
    media = MediaFileUpload(f"{link_up}", resumable=True)
    #Gửi nội dung đi
    send = service.files().create(
        body = file_metadata,
        media_body = media,
        fields = "id"
    ).execute()


def upload_image_student():
    # Đọc dữ liệu tên và số báo danh
    #Đọc dữ liệu tên
    f = open(f"data_student/file_hs_upload.txt", mode="r", encoding="utf-8-sig")
    mang = []
    info_hs = f.read()
    mang = info_hs.split(",")
    mang_xuli = []
    for i in range(3):
        dt = str(mang[i])
        dt.replace(" ", "")
        mang_xuli.append(dt)
    print("Mảng xử lí là", mang_xuli)
    name_hs = mang_xuli[0]  # Tên học sinh
    sbd_hs = mang_xuli[1]  # Số báo danh
    school_hs = mang_xuli[2]
    f.close()
    print("Tên:", name_hs)
    print("Học sinh:",sbd_hs)
    print("Trường:",school_hs)
    link_image = f"{sbd_hs}.png"
    link_up = f"Students_Fraud/{sbd_hs}.png"
    #UPDATE DATA
    service = google_drive_API()
    #Khởi tạo ID của thư mục
    folder_id_hs_vp = ["1B5iCn4hPpJoJv7Vj2ivl3qSc3YtTCrgj"]
    #Khởi tạo file học sinh
    name_link = []
    link = link_image
    name_link.append(link)
    file_name = name_link
    #Khởi tạo cấu trúc body
    file_metadata = {
        "name": file_name,
        "parents": folder_id_hs_vp
    }
    #Khởi tạo đường dẫn MEDIA
    media = MediaFileUpload(f"{link_up}", resumable=True)
    #Gửi nội dung đi
    send = service.files().create(
        body = file_metadata,
        media_body = media,
        fields = "id"
    ).execute()
f = open(f"data_student/file_hs_upload.txt", mode="r", encoding="utf-8-sig")
# mang = []
# info_hs = f.readline()
# mang = info_hs.split(",")
# mang_xuli = []
# for i in range(3):
#     dt = str(mang[i])
#     dt.replace(" ", "")
#     mang_xuli.append(dt)

# print("Mảng xử lí là", mang_xuli)
# name_hs = mang_xuli[0]  # Tên học sinh
# sbd_hs = mang_xuli[1]  # Số báo danh
# school_hs = mang_xuli[2]
# f.close()
# link_anh = f"{sbd_hs}.png"
# link_up = f"Students_Fraud/{sbd_hs}.png"
# upload_image_qr()

