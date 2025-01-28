def ghi_nhan_gian_lan():
    f = open("data_student/file_hs_vi_pham_excel.txt","r",encoding="utf-8-sig")
    a = f.read().split("\n")
    f.close()
    # print(a)
    ten = a[0]
    so_bao_danh = a[1]
    truong = a[2]
    lop = a[3]
    mon = a[4]
    #Tên học sinh
    ten = ten[14:]
    #Số báo danh
    sbd = so_bao_danh[13:]
    #Tên trường
    truong = truong[8:]
    #Tên lớp
    lop = lop[5:]
    #Môn thi
    monthi = mon[9:]
    # print("Tên là:",ten)
    # print("Lớp là:",lop)
    # print("Trường là:",truong)
    # print("Số báo danh là:",sbd)
    # print("Môn thi là:",monthi)
    # Ghi nội dung file google sheets
    import datetime
    import gspread
    from xoa_tieng_viet import no_accent_vietnamese
    # gs = gspread.service_account("history-student.json")  # Truyền nguồn dữ liệu
    # sht = gs.open_by_key("1NfVvEe3zvqQf_E0WJKPzOjXFLMwaeLGSVoJztPdmjV0")

    gs = gspread.service_account("token_gen_10012023.json")  # Truyền nguồn dữ liệu
    # sht = gs.open_by_key("1NfVvEe3zvqQf_E0WJKPzOjXFLMwaeLGSVoJztPdmjV0")
    sht = gs.open_by_key("1Zb8mKW9TAwOIAJXyXopS_ldpPcStT7G6Zno0SOJm2QI")


    # print(sht.title)  # In tiêu đề ra
    worksheet = sht.get_worksheet(1)  # Truy cập vào học sinh vi phạm
    # Kiểm tra xem trong file có nội dung không
    col_test = worksheet.row_values(1)  # Lấy giá trị dòng
    # Nếu mảng trống thì ghi tiêu đề vào
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
    # print("Dòng khả thi:", row_empty)
    # Khai báo mảng thông tin
    mang_thong_tin = []
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
    #Thêm dữ liệu vào mảng
    #Thêm tên vào mảng thông tin
    mang_thong_tin.append(ten)
    #Thêm số báo danh vào mảng thông tin
    mang_thong_tin.append(sbd)
    #Thêm tên trường vào mảng thông tin
    mang_thong_tin.append(truong)
    #Thêm lớp
    mang_thong_tin.append(lop)
    # #Thời gian vi phạm
    mang_thong_tin.append(thoi_gian_lam_bai)
    #Thêm ngày tháng làm bài vào
    mang_thong_tin.append(vao_luc)
    #Hành vi
    hanh_vi = "Hành vi quay cóp"
    #Thêm hành vi vào mảng
    mang_thong_tin.append(hanh_vi)
    #Thêm môn thi vào
    mang_thong_tin.append(monthi)
    for i in range(8):
        so_chi_muc = f"{index_content[i]}{row_empty}"
        worksheet.update_acell(so_chi_muc, mang_thong_tin[i])


    # print('Học sinh quay cóp')
#
# ghi_nhan_gian_lan()