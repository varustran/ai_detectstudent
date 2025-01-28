import time

from PyQt5.QtCore import QThread, pyqtSignal,Qt
import playsound
import keras
import cv2
import numpy as np
import mediapipe as mp
from playsound import *
from def_important import mediapipe_detection, draw_style_landmarks, extract_keypoints, send_photos_far_quay_cop, send_photos_far_sleep, send_photos_giam_sat_rong, send_photos_giam_sat_ngu


import argparse
import csv
import os
import platform
import sys
from pathlib import Path

import pathlib

pathlib.PosixPath = pathlib.WindowsPath

import torch
import asyncio

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from ultralytics.utils.plotting import Annotator, colors, save_one_box

from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
from utils.general import (
    LOGGER,
    Profile,
    check_file,
    check_img_size,
    check_imshow,
    check_requirements,
    colorstr,
    cv2,
    increment_path,
    non_max_suppression,
    print_args,
    scale_boxes,
    strip_optimizer,
    xyxy2xywh,
)
from utils.torch_utils import select_device, smart_inference_mode

import telegram  # Cài bản 13.6
so_nguoi = 0

class CameraDetectionThread(QThread):
    signal6 = pyqtSignal(np.ndarray)
    def __init__(self):
        super(CameraDetectionThread, self).__init__()
        # self.model_path = model_path
        # self.label = label
        # self.signal = signal6
        self.gg = True

    def run(self):
        self.gg = True
        f = open("Link_camera/link_data_camera.txt", mode="r", encoding="utf-8-sig")
        a = f.readline().strip()
        if str(a) == "0" or str(a) == "1" or str(a) == "2" or str(a) == "3" or str(a) == "4":
            link_cam = int(a)  # Set khi camera nhập từ phím
        else:
            link_cam = str(a)
        print(link_cam)
        self.run_program(source=link_cam)  # Hàm chạy chương trình chính
    # Hàm dừng chương trình
    def stop(self):
        self.gg = False
        self.wait()
        self.terminate()  # Hàm dừng luồng
    # Hàm cho điều kiện While True sai
    def pause_stream(self):
       pass

    def letterbox(self, im, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleup=True, stride=32):
        # Resize and pad image while meeting stride-multiple constraints
        shape = im.shape[:2]  # current shape [height, width]
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not scaleup:  # only scale down, do not scale up (for better val mAP)
            r = min(r, 1.0)

        # Compute padding
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding

        if auto:  # minimum rectangle
            dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding

        dw /= 2  # divide padding into 2 sides
        dh /= 2

        if shape[::-1] != new_unpad:  # resize
            im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
        return im, r, (dw, dh)

    # def detect(self, img_path):
    #     try:
    #     #     fcnt = 0
    #     #
    #     #     files = open("Telegram_bot/token.txt", "r")
    #     #     mang = []
    #     #     a = files.read()
    #     #     mang = a.split(",")
    #     #     mang_xuli = []
    #     #     for i in range(2):
    #     #         dt = str(mang[i])
    #     #         dt.replace(" ", "")
    #     #         mang_xuli.append(dt)
    #     #     my_token = mang[0]  # ID
    #     #     bot = telegram.Bot(token=my_token)
    #
    #         EP_list = ['CPUExecutionProvider']
    #         session = rt.InferenceSession("best_keo_dai.onnx", providers=EP_list)
    #         img = cv2.imread(img_path)
    #         origin_height, origin_width = img.shape[:2]
    #         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #         image = img.copy()
    #         image, ratio, dwdh = self.letterbox(image, auto=False)
    #         image = image.transpose((2, 0, 1))
    #         image = np.expand_dims(image, 0)
    #         image = np.ascontiguousarray(image)
    #         im = image.astype(np.float32)
    #         im /= 255
    #         inname = [i.name for i in session.get_inputs()]
    #         inp = {inname[0]: im}
    #         outputs = session.run(None, inp)[0]
    #         points = []
    #         for i, (batch_id, x0, y0, x1, y1, cls_id, score) in enumerate(outputs):
    #             box = np.array([x0, y0, x1, y1])
    #             box -= np.array(dwdh * 2)
    #             box /= ratio
    #             box = box.round().astype(np.int32).tolist()
    #             point = [int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)]
    #             points.append(point)
    #
    #             # if cnt:
    #             #     fcnt += 1
    #             # else:
    #             #     fcnt = 0
    #             # im0 = annotator.result()
    #             # # def return_img(im0):
    #             # #     return im0
    #             # #
    #             # # return_img(im0)
    #             # anh = cv2.resize(im0, (450, 250))
    #             # self.signal6.emit(anh)
    #             # if fcnt == 50:
    #             #     fcnt = 0
    #             #
    #             #     try:
    #             #         link_anh = r"Image/hoc_sinh_quay_cop1.jpg"
    #             #         cv2.imwrite(link_anh, im0)
    #             #         link_anh_1 = r"hoc_sinh_quay_cop2.jpg"
    #             #         cv2.imwrite(link_anh_1, source)
    #             #
    #             #         id = mang[1]  # Token                        # Gọi bot
    #             #         image = open(link_anh, "rb")
    #             #         image1 = open(link_anh_1, "rb")
    #             #         bot.sendPhoto(chat_id=id, photo=image, caption='Hình ảnh thí sinh gian lận')
    #             #         bot.sendPhoto(chat_id=id, photo=image1, caption='Hình ảnh thí sinh gian lận')
    #             #     except:
    #             #         pass
    #
    #         if points[0][0] > points[1][0]:
    #             point1 = [points[1][0], points[1][1]]
    #             point2 = [points[0][0], points[0][1]]
    #         else:
    #             point1 = [points[0][0], points[0][1]]
    #             point2 = [points[1][0], points[1][1]]
    #     except Exception as ex:
    #         point1 = [100, 500]
    #         point2 = [200, 500]
    #
    #     return point1, point2


    #Hàm chạy chương trình chính
    # @torch.no_grad()
    # def run_program1(self,
    #             weights=ROOT / 'weight2.pt',  # model.pt path(s)
    #             source=ROOT / 'data/images',  # file/dir/URL/glob, 0 for webcam
    #             data=ROOT / 'data/coco128.yaml',  # dataset.yaml path
    #             imgsz=(640, 640),  # inference size (height, width)
    #             conf_thres=0.25,  # confidence threshold
    #             iou_thres=0.45,  # NMS IOU threshold
    #             max_det=1000,  # maximum detections per image
    #             device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
    #             view_img=False,  # show results
    #             save_txt=False,  # save results to *.txt
    #             save_conf=False,  # save confidences in --save-txt labels
    #             save_crop=False,  # save cropped prediction boxes
    #             nosave=False,  # do not save images/videos
    #             classes=None,  # filter by class: --class 0, or --class 0 2 3
    #             agnostic_nms=False,  # class-agnostic NMS
    #             augment=False,  # augmented inference
    #             visualize=False,  # visualize features
    #             update=False,  # update all models
    #             project=ROOT / 'runs/detect',  # save results to project/name
    #             name='exp',  # save results to project/name
    #             exist_ok=False,  # existing project/name ok, do not increment
    #             line_thickness=3,  # bounding box thickness (pixels)
    #             hide_labels=False,  # hide labels
    #             hide_conf=False,  # hide confidences
    #             half=False,  # use FP16 half-precision inference
    #             dnn=False,  # use OpenCV DNN for ONNX inference
    # ):
    #     source = str(source)
    #     fcnt = 0
    #
    #     files = open("Telegram_bot/token.txt", "r")
    #     mang = []
    #     a = files.read()
    #     mang = a.split(",")
    #     mang_xuli = []
    #     for i in range(2):
    #         dt = str(mang[i])
    #         dt.replace(" ", "")
    #         mang_xuli.append(dt)
    #     my_token = mang[0]  # ID
    #     bot = telegram.Bot(token=my_token)
    #     save_img = not nosave and not source.endswith('.txt')  # save inference images
    #     is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
    #     is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
    #     webcam = source.isnumeric() or source.endswith('.txt') or (is_url and not is_file)
    #     if is_url and is_file:
    #         source = check_file(source)  # download
    #
    #     # Directories
    #     save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
    #     (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir
    #
    #     # Load model
    #     device = select_device(device)
    #     model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
    #     stride, names, pt = model.stride, model.names, model.pt
    #     imgsz = check_img_size(imgsz, s=stride)  # check image size
    #
    #     # Dataloader
    #     if webcam:
    #         view_img = check_imshow()
    #         cudnn.benchmark = True  # set True to speed up constant image size inference
    #         dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt)
    #         bs = len(dataset)  # batch_size
    #     else:
    #         dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt)
    #         bs = 1  # batch_size
    #     vid_path, vid_writer = [None] * bs, [None] * bs
    #
    #     # Run inference
    #     model.warmup(imgsz=(1 if pt else bs, 3, *imgsz))  # warmup
    #     seen, windows, dt = 0, [], [0.0, 0.0, 0.0]
    #     for path, im, im0s, vid_cap, s in dataset:
    #         if self.gg == False:
    #             return
    #         t1 = time_sync()
    #         im = torch.from_numpy(im).to(device)
    #         im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
    #         im /= 255  # 0 - 255 to 0.0 - 1.0
    #         if len(im.shape) == 3:
    #             im = im[None]  # expand for batch dim
    #         t2 = time_sync()
    #         dt[0] += t2 - t1
    #
    #         # Inference
    #         visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
    #         pred = model(im, augment=augment, visualize=visualize)
    #         t3 = time_sync()
    #         dt[1] += t3 - t2
    #
    #         # NMS
    #         pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
    #         dt[2] += time_sync() - t3
    #
    #         # Second-stage classifier (optional)
    #         # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)
    #
    #         # Process predictions
    #         for i, det in enumerate(pred):  # per image
    #             cnt = 0
    #             seen += 1
    #             if webcam:  # batch_size >= 1
    #                 p, im0, frame = path[i], im0s[i].copy(), dataset.count
    #                 s += f'{i}: '
    #             else:
    #                 p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)
    #
    #             p = Path(p)  # to Path
    #             save_path = str(save_dir / p.name)  # im.jpg
    #             txt_path = str(save_dir / 'labels' / p.stem) + (
    #                 '' if dataset.mode == 'image' else f'_{frame}')  # im.txt
    #             s += '%gx%g ' % im.shape[2:]  # print string
    #             gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
    #             imc = im0.copy() if save_crop else im0  # for save_crop
    #             annotator = Annotator(im0, line_width=line_thickness, example=str(names))
    #             if len(det):
    #                 # Rescale boxes from img_size to im0 size
    #                 det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()
    #
    #                 # Print results
    #                 for c in det[:, -1].unique():
    #                     n = (det[:, -1] == c).sum()  # detections per class
    #                     s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
    #
    #                 # Write results
    #                 for *xyxy, conf, cls in reversed(det):
    #                     if save_txt:  # Write to file
    #                         xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(
    #                             -1).tolist()  # normalized xywh
    #                         line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
    #                         with open(f'{txt_path}.txt', 'a') as f:
    #                             f.write(('%g ' * len(line)).rstrip() % line + '\n')
    #
    #                     if save_img or save_crop or view_img:  # Add bbox to image
    #                         c = int(cls)  # integer class
    #                         label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
    #                         annotator.box_label(xyxy, label, color=colors(c, True))
    #                     if save_crop:
    #                         save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)
    #                     c = int(cls)  # integer class
    #                     label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
    #                     lst = label.split(' ')
    #                     try:
    #                         if (c == 1 and len(lst) > 1 and float(lst[1]) >= 0.32):
    #                             # print("haha", lst[1])4
    #                             cnt += 1
    #                     except:
    #                         pass
    #                     if cnt:
    #                         fcnt += 1
    #                     else:
    #                         fcnt = 0
    #                     im0 = annotator.result()
    #                     # def return_img(im0):
    #                     #     return im0
    #                     #
    #                     # return_img(im0)
    #                     anh = cv2.resize(im0, (450, 250))
    #                     self.signal6.emit(anh)
    #                     if fcnt == 25:
    #                         fcnt = 0
    #
    #                         try:
    #                             link_anh = r"Image/hoc_sinh_quay_cop1.jpg"
    #                             cv2.imwrite(link_anh, im0)
    #                             # link_anh_1 = r"hoc_sinh_quay_cop2.jpg"
    #                             # cv2.imwrite(link_anh_1, source)
    #
    #                             id = mang[1]  # Token                        # Gọi bot
    #                             image = open(link_anh, "rb")
    #                             # image1 = open(link_anh_1, "rb")
    #                             bot.sendPhoto(chat_id=id, photo=image, caption='Hình ảnh thí sinh gian lận')
    #                         #     bot.sendPhoto(chat_id=id, photo=image1, caption='Hình ảnh thí sinh gian lận')
    #                         except:
    #                             pass
    #             # Stream results
    #
    #             # signal.emit(im0)
    #             # print(signal)
    #             # if view_img:
    #             #     if p not in windows:
    #             #         windows.append(p)
    #             #         cv2.namedWindow(str(p), cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
    #             #         cv2.resizeWindow(str(p), im0.shape[1], im0.shape[0])
    #             #     cv2.imshow(str(p), im0)
    #             #     cv2.waitKey(1)  # 1 millisecond
    #
    #             # Save results (image with detections)
    #             if save_img:
    #                 if dataset.mode == 'image':
    #                     cv2.imwrite(save_path, im0)
    #                 else:  # 'video' or 'stream'
    #                     if vid_path[i] != save_path:  # new video
    #                         vid_path[i] = save_path
    #                         if isinstance(vid_writer[i], cv2.VideoWriter):
    #                             vid_writer[i].release()  # release previous video writer
    #                         if vid_cap:  # video
    #                             fps = vid_cap.get(cv2.CAP_PROP_FPS)
    #                             w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    #                             h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #                         else:  # stream
    #                             fps, w, h = 30, im0.shape[1], im0.shape[0]
    #                         save_path = str(
    #                             Path(save_path).with_suffix('.mp4'))  # force *.mp4 suffix on results videos
    #                         vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
    #                     vid_writer[i].write(im0)
    #
    #         # Print time (inference-only)
    #         LOGGER.info(f'{s}Done. ({t3 - t2:.3f}s)')
    #
    #     # Print results
    #     t = tuple(x / seen * 1E3 for x in dt)  # speeds per image
    #     LOGGER.info(
    #         f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)
    #     if save_txt or save_img:
    #         s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
    #         LOGGER.info(f"Results saved to {colorstr('bold', save_dir)}{s}")
    #     if update:
    #         strip_optimizer(weights)  # update model (to fix SourceChangeWarning)
    #     if self.gg == False:
    #         return
    @smart_inference_mode()
    def run_program(self,
        weights=ROOT / "best.pt",  # model path or triton URL
        source=ROOT / "data/images",  # file/dir/URL/glob/screen/0(webcam)
        data=ROOT / "data/coco128.yaml",  # dataset.yaml path
        imgsz=(640, 640),  # inference size (height, width)
        conf_thres=0.25,  # confidence threshold
        iou_thres=0.45,  # NMS IOU threshold
        max_det=1000,  # maximum dete ctions per image
        device="",  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        view_img=False,  # showresults
        save_txt=False,  # save results to *.txt
        save_csv=False,  # save results in CSV format
        save_conf=False,  # save confidences in --save-txt labels
        save_crop=False,  # save cropped prediction boxes
        nosave=False,  # do not save images/videos
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        augment=False,  # augmented inference
        visualize=False,  # visualize features
        update=False,  # update all models
        project=ROOT / "runs/detect",  # save results to project/name
        name="exp",  # save results to project/name
        exist_ok=False,  # existing project/name ok, do not increment
        line_thickness=3,  # bounding box thickness (pixels)
        hide_labels=False,  # hide labels
        hide_conf=False,  # hide confidences
        half=False,  # use FP16 half-precision inference
        dnn=False,  # use OpenCV DNN for ONNX inference
        vid_stride=1,  # video frame-rate stride
    ):
        source = str(source)
        fcnt = 0
        cnt = 0

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
        bot = telegram.Bot(token=my_token)

        save_img = not nosave and not source.endswith(".txt")  # save inference images
        is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
        is_url = source.lower().startswith(("rtsp://", "rtmp://", "http://", "https://"))
        webcam = source.isnumeric() or source.endswith(".streams") or (is_url and not is_file)
        screenshot = source.lower().startswith("screen")
        if is_url and is_file:
            source = check_file(source)  # download

        # Directories
        save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
        (save_dir / "labels" if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

        # Load model
        device = select_device(device)
        model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
        stride, names, pt = model.stride, model.names, model.pt
        imgsz = check_img_size(imgsz, s=stride)  # check image size

        # Dataloader
        bs = 1  # batch_size
        if webcam:
            view_img = check_imshow(warn=True)
            dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
            bs = len(dataset)
        elif screenshot:
            dataset = LoadScreenshots(source, img_size=imgsz, stride=stride, auto=pt)
        else:
            dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
        vid_path, vid_writer = [None] * bs, [None] * bs

        # Run inference
        model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup
        seen, windows, dt = 0, [], (Profile(device=device), Profile(device=device), Profile(device=device))
        for path, im, im0s, vid_cap, s in dataset:
            with dt[0]:
                im = torch.from_numpy(im).to(model.device)
                im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
                im /= 255  # 0 - 255 to 0.0 - 1.0
                if len(im.shape) == 3:
                    im = im[None]  # expand for batch dim
                if model.xml and im.shape[0] > 1:
                    ims = torch.chunk(im, im.shape[0], 0)

            # Inference
            with dt[1]:
                visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
                if model.xml and im.shape[0] > 1:
                    pred = None
                    for image in ims:
                        if pred is None:
                            pred = model(image, augment=augment, visualize=visualize).unsqueeze(0)
                        else:
                            pred = torch.cat((pred, model(image, augment=augment, visualize=visualize).unsqueeze(0)), dim=0)
                    pred = [pred, None]
                else:
                    pred = model(im, augment=augment, visualize=visualize)
            # NMS
            with dt[2]:
                pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

            # Second-stage classifier (optional)
            # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

            # Define the path for the CSV file
            csv_path = save_dir / "predictions.csv"

            # Create or append to the CSV file
            def write_to_csv(image_name, prediction, confidence):
                """Writes prediction data for an image to a CSV file, appending if the file exists."""
                data = {"Image Name": image_name, "Prediction": prediction, "Confidence": confidence}
                with open(csv_path, mode="a", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=data.keys())
                    if not csv_path.is_file():
                        writer.writeheader()
                    writer.writerow(data)

            # Process predictions
            for i, det in enumerate(pred):  # per image
                seen += 1
                if webcam:  # batch_size >= 1
                    p, im0, frame = path[i], im0s[i].copy(), dataset.count
                    s += f"{i}: "
                else:
                    p, im0, frame = path, im0s.copy(), getattr(dataset, "frame", 0)

                p = Path(p)  # to Path
                save_path = str(save_dir / p.name)  # im.jpg
                txt_path = str(save_dir / "labels" / p.stem) + ("" if dataset.mode == "image" else f"_{frame}")  # im.txt
                s += "%gx%g " % im.shape[2:]  # print string
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                imc = im0.copy() if save_crop else im0  # for save_crop
                annotator = Annotator(im0, line_width=line_thickness, example=str(names))
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, 5].unique():
                        n = (det[:, 5] == c).sum()  # detections per class
                        s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                    # Write results
                    for *xyxy, conf, cls in reversed(det):
                        c = int(cls)  # integer class
                        label = names[c] if hide_conf else f"{names[c]}"
                        confidence = float(conf)
                        confidence_str = f"{confidence:.2f}"

                        if save_csv:
                            write_to_csv(p.name, label, confidence_str)

                        if save_txt:  # Write to file
                            xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                            line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                            with open(f"{txt_path}.txt", "a") as f:
                                f.write(("%g " * len(line)).rstrip() % line + "\n")

                        if save_img or save_crop or view_img:  # Add bbox to image
                            c = int(cls)  # integer class
                            label = None if hide_labels else (names[c] if hide_conf else f"{names[c]} {conf:.2f}")
                            annotator.box_label(xyxy, label, color=colors(c, True))
                        if save_crop:
                            save_one_box(xyxy, imc, file=save_dir / "crops" / names[c] / f"{p.stem}.jpg", BGR=True)
                        c = int(cls)  # integer class
                        label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                        lst = label.split(' ')
                        try:
                            if (c == 1 and len(lst) > 1 and float(lst[1]) >= 0.8):
                                # print("haha", lst[1])
                                cnt += 1
                        except:
                            pass
                    if cnt:
                        fcnt += 1
                    else:
                        fcnt = 0
                    cnt = 0
                    im0 = annotator.result()
                    # def return_img(im0):
                    #     return im0
                    #
                    # return_img(im0)
                    anh = cv2.resize(im0, (450, 250))
                    self.signal6.emit(anh)
                    if fcnt == 50:
                        fcnt = 0

                        cnt = 0
                        while cnt < 5:
                            try:
                                playsound("yeucau.m4a")
                                link_anh = r"Image/hoc_sinh_quay_cop1.jpg"
                                cv2.imwrite(link_anh, im0)
                                # link_anh_1 = r"hoc_sinh_quay_cop2.jpg"
                                # cv2.imwrite(link_anh_1, source)

                                id = mang[1]  # Token                        # Gọi bot
                                image = open(link_anh, "rb")
                                # image1 = open(link_anh_1, "rb")
                                asyncio.run(bot.sendPhoto(chat_id=id, photo=image,
                                                          caption='Hình ảnh thí sinh gian lận, ô ghi chữ not_cheating là thì sinh không gian lận còn nếu là Cheating thì gian lận'))
                                time.sleep(1)
                                break
                            #     bot.sendPhoto(chat_id=id, photo=image1, caption='Hình ảnh thí sinh gian lận')
                            except:
                                time.sleep(1)
                                cnt += 1
                # Stream results
                im0 = annotator.result()
                if view_img:
                    if platform.system() == "Linux" and p not in windows:
                        windows.append(p)
                        cv2.namedWindow(str(p), cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
                        cv2.resizeWindow(str(p), im0.shape[1], im0.shape[0])
                    cv2.imshow(str(p), im0)
                    cv2.waitKey(1)  # 1 millisecond

                # Save results (image with detections)
                if save_img:
                    if dataset.mode == "image":
                        cv2.imwrite(save_path, im0)
                    else:  # 'video' or 'stream'
                        if vid_path[i] != save_path:  # new video
                            vid_path[i] = save_path
                            if isinstance(vid_writer[i], cv2.VideoWriter):
                                vid_writer[i].release()  # release previous video writer
                            if vid_cap:  # video
                                fps = vid_cap.get(cv2.CAP_PROP_FPS)
                                w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                                h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                            else:  # stream
                                fps, w, h = 30, im0.shape[1], im0.shape[0]
                            save_path = str(Path(save_path).with_suffix(".mp4"))  # force *.mp4 suffix on results videos
                            vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
                        vid_writer[i].write(im0)

                if self.gg == False:
                    return

            # Print time (inference-only)
            LOGGER.info(f"{s}{'' if len(det) else '(no detections), '}{dt[1].dt * 1E3:.1f}ms")

        # Print results
        t = tuple(x.t / seen * 1e3 for x in dt)  # speeds per image
        LOGGER.info(f"Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}" % t)
        if save_txt or save_img:
            s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ""
            LOGGER.info(f"Results saved to {colorstr('bold', save_dir)}{s}")
        if update:
            strip_optimizer(weights[0])  # update model (to fix SourceChangeWarning)
        if self.gg == False:
            return

class detect_far(QThread):
    signal6 = pyqtSignal(np.ndarray)
    def __init__(self, index):
        super(detect_far, self).__init__()
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
        cv2.destroyAllWindows()
        self.terminate()  # Hàm dừng luồng

    # Hàm cho điều kiện While True sai
    def pause_stream(self):
       pass

    #Hàm chạy chương trình chính
    def run_program(self):

        print("Nhận luồng")
        mp_holistic = mp.solutions.holistic #Khởi tạo hàm nhận dạng
        #Load model
        model = keras.models.load_model('hanhdong.h5') # ví dụ: đọc mô hình từ tệp h5
        # model1 = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        # Khởi tạo cấu trúc vẽ
        mp_drawing = mp.solutions.drawing_utils
        sequence = []   #Mảng chứa tên hành động
        sentence = []   #Mảng chứa độ chính xác
        actions = np.array(["Dang kiem tra", "Quay cop","Ngu"])
        threshold = 0.5 #Độ chính xác cần nhận dạng
        predictions = []
        colors = [(245,117,16), (117,245,16), (16,117,245)] #Bảng màu sắc

        #Hàm vẽ các hành động trên cam
        def prob_viz(res, actions, input_frame, colors):
            output_frame = input_frame.copy()
            # for num, prob in enumerate(res):
            #     cv2.rectangle(output_frame, (0,60+num*40), (int(prob*100), 90+num*40), colors[num], -1)
            #     cv2.putText(output_frame, actions[num], (0, 85+num*40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            return output_frame
        #Đọc dữ liệu cho camera
        f = open("Link_camera/link_data_camera.txt",mode = "r",encoding="utf-8-sig")
        a = f.readline().strip()
        if str(a) == "0" or str(a) == "1" or str(a) == "2" or str(a) == "3" or str(a) == "4":
            link_cam = int(a)   #Set khi camera nhập từ phím
        else:
            link_cam = str(a)
        print(link_cam)
        # with yolo.run(source = link_cam) as yolov5:


        cap = cv2.VideoCapture(link_cam)    #Lấy camera
        # Mảng điều kiện
        fraud = 0  # Mảng chứa số lần quay cóp
        sleep = 0  # Mảng chứa số lần ngủ
        kiem_tra_quay_cop = 0
        kiem_tra_ngu = 0
        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

            while True:
                # Đọc camera
                ret, frame = cap.read()

                # Lấy toạ độ các điểm
                image, results = mediapipe_detection(frame, holistic)
                # print(results)
                # Vẽ các điểm lên cơ thể
                draw_style_landmarks(image, results)

                # Logic tính toán
                keypoints = extract_keypoints(results)
                sequence.append(keypoints)
                sequence = sequence[-30:]
                # Điều kiện thoả mãn nhận dạng
                if len(sequence) == 30:
                    res = model.predict(np.expand_dims(sequence, axis=0))[0]
                    # print(actions[np.argmax(res)])
                    predictions.append(np.argmax(res))

                    if np.unique(predictions[-10:])[0] == np.argmax(res):
                        if res[np.argmax(res)] > threshold:
                            if len(sentence) > 0:
                                if actions[np.argmax(res)] != sentence[-1]:
                                    sentence.append(actions[np.argmax(res)])
                            else:
                                sentence.append(actions[np.argmax(res)])

                    if len(sentence) > 5:
                        sentence = sentence[-5:]

                    # # Viz probabilities
                    image = prob_viz(res, actions, image, colors)

                # Hiển thị camera
                anh = cv2.resize(image, (450, 250))
                # cv2.imshow('OpenCV Feed', anh)
                # Trả dữ liệu về luồng
                print("Bắt đầu trả về dữ liệu")
                self.signal6.emit(anh)
                print("Kết thúc trả về dữ liệu")
                # Hàm kiểm tra
                if len(sentence) != 0:
                    print("Hành động là:", sentence[0])
                    # Điều kiện chính
                    if str(sentence[0]) == "Dang kiem tra":
                        pass
                    elif str(sentence[0]) == "Ngu":
                        sleep += 1

                    elif str(sentence[0]) == "Quay cop":
                        fraud += 1

                #Điều kiện phát hiện gian lận

                #Điều kiện nhắc nhở:
                if sleep > 30:
                    print("Dừng ngủ")
                    playsound.playsound("Audio/sleep.mp3")
                    cv2.waitKey(5000)
                    sleep = 0
                    kiem_tra_ngu += 1
                    cv2.imwrite("Image/hoc_sinh_ngu.png", frame)
                    send_photos_giam_sat_rong()
                if fraud > 30:
                    print("Dừng quay cóp")
                    playsound.playsound("Audio/nghiemtuc.mp3")
                    kiem_tra_quay_cop += 1
                    fraud = 0
                    cv2.imwrite("Image/hoc_sinh_ngu.png", frame)
                    send_photos_giam_sat_rong()
                    #Điều kiện phát hiện quay cóp
                if kiem_tra_quay_cop >=3:
                    playsound.playsound("Audio/fraud.mp3")
                    # cv2.imwrite("Image/hoc_sinh_quay_cop.png",frame)
                    cv2.imwrite("Image/hoc_sinh_ngu.png",frame)
                    send_photos_giam_sat_rong()
                    break

                if kiem_tra_ngu >=8:
                    playsound.playsound("Audio/thong_bao.mp3")
                    cv2.imwrite("Image/hoc_sinh_rong.png",frame)
                    send_photos_giam_sat_ngu()
                    break
                if self.gg == False:
                    break

        cap.release()
        cv2.destroyAllWindows()
        self.quit()
        self.wait()
