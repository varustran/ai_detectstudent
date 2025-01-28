#Ghi nhận gian lận
def ghi_nhan_che_cam():
    # Ghi nội dung file google sheets
    import datetime
    import gspread
    from xoa_tieng_viet import no_accent_vietnamese
    gs = gspread.service_account("token_gen_10012023.json")  # Truyền nguồn dữ liệu
    sht = gs.open_by_key("1Zb8mKW9TAwOIAJXyXopS_ldpPcStT7G6Zno0SOJm2QI")
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
    loaihinh = "Hành vi che camera"
    # Thêm nội dung vào mảng
    mang_thong_tin.append(loaihinh)
    mang_thong_tin.append(mon)
    for i in range(8):
        so_chi_muc = f"{index_content[i]}{row_empty}"
        worksheet.update(so_chi_muc, mang_thong_tin[i])
ghi_nhan_che_cam()