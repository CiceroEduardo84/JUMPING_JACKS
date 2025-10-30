import cv2

def windowCurrentSize(window):
  # Descobre o tamanho atual da janela
  window_w = cv2.getWindowImageRect(window)[2]
  window_h = cv2.getWindowImageRect(window)[3]
  
  return window_w, window_h