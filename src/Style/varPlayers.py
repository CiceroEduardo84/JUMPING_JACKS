import mediapipe as mp
import cv2

mp_draw = mp.solutions.drawing_utils

# Player variables styles
PLAYER_COLOR1 = (255, 0, 0)
PLAYER_COLOR2 = (0, 255, 0)
PLAYERS_LINES_COLOR = (255,255,255)
PLAYERS_CONFIG_LINES = mp_draw.DrawingSpec(color=PLAYERS_LINES_COLOR, thickness=2)
PLAYER_CONFIG_COLOR1 = mp_draw.DrawingSpec(color=PLAYER_COLOR1, thickness=2, circle_radius=3)
PLAYER_CONFIG_COLOR2 = mp_draw.DrawingSpec(color=PLAYER_COLOR2, thickness=2, circle_radius=3)

# Game variables styles
TEXT_COLOR_WHITE=(255, 255, 255)
TEXT_COLOR_RED = (0, 0, 255)
TEXT_SCALE_COUNT = 1
TEXT_SIZE_CAUNT= 3
TEXT_STYLE_CAUNT = cv2.FONT_HERSHEY_SIMPLEX