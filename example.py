"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(1)

while True:
    # We get a new frame from the webcam
    _, frame1 = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame1)

    frame1 = gaze.annotated_frame()
    text_1 = ""

    if gaze.is_blinking():
        text = "Blinking"
        #testing to the moon
    elif gaze.is_right():
        text = "Phai"
    elif gaze.is_left():
        text = "Trai"
    elif gaze.is_center():
        text = "Chinh Giua"

    cv2.putText(frame1, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame1, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame1, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame1)

    if cv2.waitKey(1) == 27:
        break
   
webcam.release()
cv2.destroyAllWindows()
