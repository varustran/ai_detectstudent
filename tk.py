from playsound import *
from DEF_NEW import *
cam = cv2.VideoCapture(0)
#set kích thước cam
cam.set(3,640)
cam.set(4,480)
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)
#Mở file chứa thông tin học sinh ra
f = open("info_student/model.csv", mode= "r",encoding = "utf-8-sig")
#Đọc dòng thứ 1 của file
header = f.readline().strip()
#Tạo mảng chưa data học sinh
data_hocsinh = []
#Đọc dòng thứ 2
row = f.readline().strip()
#Nếu dòng thứ 2 khác rỗng thì
while row != "":
    data_hocsinh.append(row) #Thêm dòng hiện hành vào mảng data học sinh
    row = f.readline().strip()  #Đọc dòng tiếp theo để kiểm tra
        #In mảng học sinh ra màn hình
print(data_hocsinh)
#Khởi tạo mảng tên
mang_ten = []
f.close()


#Dùng vòng lặp for để xử lí tên
for i in data_hocsinh:
    mang_tam = i.split(",")
    #Thêm tên hiển thị vào biến tên
    mang_ten.append(mang_tam[5])
names = mang_ten
#Lấy số báo danh
mang_so_bao_danh = load_numbers()

#Màu vàng
yellow = (255,255,0)
pink = (255,0,255)
red = (255,0,0)
green = (0,255,0)
i = 0

dectector = cv2.QRCodeDetector()  # Nhận dạng
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')
cascadePath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    ret, frame = cam.read()
    image = cv2.resize(frame,(600,400))
    height, width = frame.shape[:2]
    # Tính toán vị trí chia ảnh thành hai phần
    split_point = width // 2
    # Chia ảnh thành hai phần
    left_image = frame[:, :split_point]
    right_image = frame[:, split_point:]
    #Lấy tên từ khuôn mặt
    print('Tới bước lấy dữ liệu khuôn mặt')
    khuon_mat = load_face(right_image,names,minW,minH,font,recognizer,faceCascade)
    #Lấy ID từ khuôn mặt
    print("Tới bước lấy ID từ khuôn mặt")
    so_bao_danh = load_faces_numbers(right_image,mang_so_bao_danh,minW,minH,recognizer,faceCascade)
    print("Số báo danh học sinh là",so_bao_danh)
    mang_du_lieu = return_data_in_list(so_bao_danh)
    print("Mảng dữ liệu là",mang_du_lieu)
    print("Tới bước đọc dữ liệu trong mã QR")
    print("Dữ liệu học sinh là",mang_du_lieu)
    if mang_du_lieu[0] != "":
        print("Có người xuất hiện")
        list_data_qr = return_list_qr_data(left_image,dectector)
        cv2.imshow("Camera left",left_image)
    else:
        print("Không có mã QR")
        cv2.imshow("Camera left",left_image)


    cv2.imshow("Camera right",khuon_mat)
    if cv2.waitKey(1) == ord("q"):
        break
cam.release()
cv2.destroyAllWindows()