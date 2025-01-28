import datetime
from xoa_tieng_viet import no_accent_vietnamese
import gspread
gs = gspread.service_account("database_dtf.json")    #Truyền nguồn dữ liệu
sht = gs.open_by_key("18bkFBKlS9mFePnsBEPCPMSejL7Yx_nfMiki427JEJVA")
worksheet = sht.get_worksheet(0)    #Lấy nội dung trong file
print(sht.title)
#Kiểm tra xem trong file có nội dung không
col_test = worksheet.col_values(1)  #Lấy giá trị dòng
#Nếu mảng trống thì ghi tiêu đề vào
if len(col_test) == 0:
    tieu_de = ["STT","Tên hiển thị","Tên đăng nhập","Mật khẩu","Số điện thoại","Email","Ngày tạo tài khoản"]
    so_tieu_de = ["A1","B1","C1","D1","E1","F1","G1"]
    worksheet.format("A1:G1", {
    # "backgroundColor": {
    #   "red": 0,
    #   "green": 255.0,
    #   "blue": 0.0
    # },
    "horizontalAlignment": "CENTER",})
    # "textFormat": {
    #   # "foregroundColor": {
    #   #   "red": 1.0,
    #   #   "green": 1.0,
    #   #   "blue": 1.0
    #   # },
    #   "fontSize": 13,
    #   "bold": True
    # }
    # })
    #Ghi tiêu đề vào file
    for i in range(7):
        worksheet.update(so_tieu_de[i],tieu_de[i])  #Ghi file
else:
    pass