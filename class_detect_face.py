
import cv2
import numpy as np

from PyQt5.QtCore import pyqtSignal, QThread
from DEF_NEW import *
from def_important import *
from playsound import *
class detect_face_class(QThread):
    signal4 = pyqtSignal(np.ndarray)
    signal5 = pyqtSignal(object)
    def __init__(self, index):
        super(detect_face_class, self).__init__()
        self.device = None
        # self.out_file = None
        self.classes = None
        # self.model = None
        self.gg = True
        self.player = None
        self.index = index
    # Hàm chạy luồng
    def run(self):
        self.gg = True
        self.run_program()  # Hàm chạy chương trình chính

    # Hàm dừng chương trình
    def stop(self):
        self.gg = False
        self.wait()
        cv2.destroyAllWindows()  # Huỷ cửa sổ Camera
        self.terminate()
    # Hàm cho điều kiện While True sai
    def pause_stream(self):
        pass

    #Hàm chạy chương trình chính
    # def run_program(self):
    #     kiemtra = True
    #     print("Chạy luồng 4")
    #     recognizer = cv2.face.LBPHFaceRecognizer_create()
    #     recognizer.read('trainer.yml')
    #     cascadePath = 'haarcascade_frontalface_default.xml'
    #     faceCascade = cv2.CascadeClassifier(cascadePath)
    #
    #     font = cv2.FONT_HERSHEY_SIMPLEX
    #     #Khởi tạo biến ID
    #     id = 0
    #     #Đọc file cam
    #     f = open("link_camera/link_cam_detect.txt", mode = "r", encoding="utf-8-sig")
    #     link = f.readline().strip()
    #     f.close()
    #     if link == "0" or link == "1" or link == "2":
    #         link = int(link)
    #     else:
    #         link = link
    #
    #     #Mở file chứa thông tin học sinh ra
    #     f = open("info_student/model.csv", mode= "r",encoding = "utf-8-sig")
    #     #Đọc dòng thứ 1 của file
    #     header = f.readline().strip()
    #     #In thử dòng thứ 1 ra
    #     print(header)
    #     #Tạo mảng chưa data học sinh
    #     data_hocsinh = []
    #     #Đọc dòng thứ 2
    #     row = f.readline().strip()
    #     #Nếu dòng thứ 2 khác rỗng thì
    #     while row != "":
    #         data_hocsinh.append(row) #Thêm dòng hiện hành vào mảng data học sinh
    #         row = f.readline().strip()  #Đọc dòng tiếp theo để kiểm tra
    #     #In mảng học sinh ra màn hình
    #     # print(data_hocsinh)
    #     #Khởi tạo mảng tên
    #     mang_ten = []
    #     f.close()
    #     #Dùng vòng lặp for để xử lí tên
    #     for i in data_hocsinh:
    #         mang_tam = i.split(",")
    #         # print(mang_tam)
    #         mang_ten.append(mang_tam[5])    #Thêm tên hiển thị vào biến tên
    #     #khai báo biến tên và gán giá trị mảng tên vào
    #     names = mang_ten
    #     #In link lấy được vào
    #     # print(f"Lấy được link rồi link là {link}")
    #     #In cam ra màn hình
    #     cam = cv2.VideoCapture(link)
    #     #set kích thước cam
    #     cam.set(3,640)
    #     cam.set(4,480)
    #     minW = 0.1 * cam.get(3)
    #     minH = 0.1 * cam.get(4)
    #     mang_so_bao_danh = load_numbers()
    #     count_face_tam = 0
    #     while True:
    #         ret, frame = cam.read()
    #         img = cv2.flip(frame,1)
    #         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #         faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize = (int(minW), int(minH)))
    #
    #         for (x, y, w, h) in faces:
    #             cv2.rectangle(img,(x,y), (x + w, y + h), (0, 255, 0),2)
    #             id, confidence = recognizer.predict(gray[y:y + h, x: w + x])
    #             # print("Loại confidence là",type(confidence))
    #             so = confidence
    #             print("conf:", confidence)
    #             if (confidence < 100):
    #                 id = names[id]
    #                 confidence = "  {0}%".format(round(100 - confidence))
    #                 name = confidence
    #                 # print("Tên là",id)
    #                 # print("Độ chính xác",name)
    #             else:
    #                 id = "Chua xac dinh"
    #                 confidence = "  {0}%".format(round(100 - confidence))
    #
    #             cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255,255,255),2)
    #             cv2.putText(img, str(confidence),(x + 5, y + h - 5), font, 1, (255,255,0),1)
    #
    #
    #
    #
    #
    #
    #
    #         self.signal4.emit(img)
    #         #Đọc mảng và set tên
    #         f = open("info_student/model.csv", mode= "r",encoding = "utf-8-sig")
    #         header = f.readline().strip()   #Kiểm tra dòng excel
    #         # print(header)   #In thử dòng đầu trong file excel
    #         data_hocsinh = []   #Tạo mảng chứa tên học sinh
    #         row = f.readline().strip()  #Đọc dữ liệu trong dòng và xử lí
    #         while row != "":    #Nếu dòng khác rỗng
    #             data_hocsinh.append(row)    #Thêm nội dung ở dòng hiện tại vào mảng data học sinh
    #             row = f.readline().strip()  #Đọc dòng tiếp theo
    #             # print(data_hocsinh)
    #             mang_ten = []
    #
    #         f.close()
    #         for i in data_hocsinh:
    #             mang_tam = i.split(",")
    #             # print(mang_tam)
    #             mang_ten.append(mang_tam[5])
    #             names = mang_ten
    #         # print("Mảng tên là")
    #         # print(mang_ten)
    #         #Xử lí so sánh mảng
    #         #Lấy tên hiển thị
    #         # print("Mảng tên đã trích lọc:",mang_ten)
    #         ten_hien_thi = id
    #         print("ID của học sinh là",id)
    #         # print("Tên hiển thị đang fix là:",ten_hien_thi)
    #         #Tạo mảng data
    #         mang_data = []
    #         #Khai báo biến tên
    #         name = ""
    #         #Khai báo số báo danh
    #         sbd = ""
    #         #Khai báo lớp
    #         lop = ""
    #         #Khai báo trường
    #         truong = ""
    #         for i in data_hocsinh:
    #             mang_tam = i.split(",")
    #             for j in range(len(mang_tam)):
    #                 if mang_tam[j] == ten_hien_thi:
    #                     name = mang_tam[1]
    #                     sbd = mang_tam[2]
    #                     lop = mang_tam[3]
    #                     truong = mang_tam[4]
    #                 else:
    #                     mang_data = []
    #             # print(mang_tam)
    #             mang_ten.append(mang_tam[5])
    #             names = mang_ten
    #         #Thêm tên vào mảng dữ liệu
    #         mang_data.append(name)
    #         #Them báo danh vào mảng dữ liệu
    #         mang_data.append(sbd)
    #         #Thêm lớp vào mảng dữ liệu
    #         mang_data.append(lop)
    #         #Thêm tên trường vào mảng dữ liệu
    #         mang_data.append(truong)
    #         print("Mảng data lúc này là",mang_data)
    #         #Truyền mảng dữ liệu đi lên
    #
    #         so_bao_danh = load_faces_numbers(frame,names,minW,minH,recognizer,faceCascade)
    #         if so_bao_danh != None:
    #             count_face_tam += 1
    #         else:
    #             count_face_tam = 0
    #             mang_data = ["","","",""]
    #         self.signal5.emit(mang_data)
    #         print("Số báo danh là",so_bao_danh)
    #         print("Số lượt đếm là",count_face_tam)
    #         if count_face_tam == 30:
    #             playsound("Audio/da_phat_hien_hoc_sinh.mp3")
    #         elif count_face_tam == 40:
    #             playsound("Audio/ba.mp3")
    #         elif count_face_tam == 45:
    #             playsound("Audio/hai.mp3")
    #         elif count_face_tam == 50:
    #             playsound("Audio/mot.mp3")
    #         elif count_face_tam >55:
    #             print(f"{name}/{sbd}/{truong}/{lop}")
    #             diem_danh_hoc_sinh(name,sbd,truong,lop)
    #             playsound("Audio/thanhcong.mp3")
    #             count_face_tam = 0
    #
    #         if self.gg == False:
    #             break
    #     cam.release()
    #     cv2.destroyAllWindows()




