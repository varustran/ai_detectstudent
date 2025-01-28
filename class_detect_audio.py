import time
import speech_recognition
import pyaudio

from DEF_NEW import *
from PyQt5.QtCore import QThread, pyqtSignal, QMutex, QWaitCondition
from playsound import playsound
import speech_recognition
from playsound import playsound
class detect_audio(QThread):
    signal_audio = pyqtSignal(np.ndarray)
    signal_giam_sat = pyqtSignal(object)
    signal_thong_bao_am_thanh = pyqtSignal(object)
    def __init__(self, index):
        super(detect_audio, self).__init__()
        self.device = None
        # self.out_file = None
        self.classes = None
        # self.model = None
        self.gg = True
        self.player = None
        self.index = index
        self.ngung = True
    # Hàm chạy luồng
    def run(self):
        # print("Bắt đầu chạy luồng âm thanh")
        self.gg = True
        self.run_program()  # Hàm chạy chương trình chính

    # Hàm dừng chương trình
    def stop(self):
        print("Dừng luồng giám sát âm thanh")
        self.gg = False
        self.wait()
        self.terminate()  # Hàm dừng luồng
    # Hàm cho điều kiện While True sai
    def pause_stream(self):
       self.ngung = False
    #Hàm chạy chương trình chính
    def run_program(self):
        # print("Bắt đầu luồng giám sát âm thanh")
        am_thanh = 0
        while True:
            if self.ngung == False:
                print("Đang dừng lắng nghe")
                time.sleep(3)
                self.ngung = True
            else:
                # khởi tạo
                ai_brain = " " # Ban đầu nó chưa được học gì cả nên cũng chưa có thông tin
                ai_ear = speech_recognition.Recognizer() # nghe người dùng nói
                you = "" # Lời nói người dùng
                # print("Khởi động mic")
                with speech_recognition.Microphone() as mic:
                    print("AI: Đang nghe")
                    audio = ai_ear.record(mic, duration = 5)
                    try:
                        print("Giá trị của ngung la",self.ngung)
                        if self.ngung == True:
                            # Nghe giọng nói của người Việt
                            you = ai_ear.recognize_google(audio, language = 'vi-VN')
                            print(you)
                            am_thanh += 1
                            if am_thanh == 1:
                                self.signal_thong_bao_am_thanh.emit(1)


                            elif am_thanh == 2:
                               self.signal_thong_bao_am_thanh.emit(2)
                            elif am_thanh == 3:
                                dung_giam_sat = "Dung"
                                self.signal_giam_sat.emit(dung_giam_sat)
                                self.signal_thong_bao_am_thanh.emit(3)
                                # send_photos()
                                send_photos_du_phong()
                                send_file_text()
                                ghi_nhan_trao_doi()
                        else:
                            pass

                    except:
                        pass
            if self.gg == False:
                break
        self.quit()
        self.wait()