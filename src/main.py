from UI import *
from Config.variablesConfig import USEVIDEO
import cv2

window = "JUMPING_JACKS"
video = cv2.VideoCapture(USEVIDEO)

cv2.namedWindow(window, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window, cv2.WINDOW_NORMAL, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window, 640, 540)

home_screen(video, window)

video.release()
cv2.destroyAllWindows()