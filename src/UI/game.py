import cv2
import mediapipe as mp
import UI
import time

from Modules.windowCurrentSize import windowCurrentSize
from Modules.processPlayers import processPlayers
from Config.variablesConfig import TIME_WINNER
from Style.varScreens import LINE_COLOR_WITH, THICKNESS_LINE


def game_player(video, window, game_mode, w, h):
    pose_module = mp.solutions.pose
    draw = mp.solutions.drawing_utils

    # Modelos de detecção
    pose_detect1 = pose_module.Pose(min_tracking_confidence=0.5, min_detection_confidence=0.5)
    pose_detect2 = pose_module.Pose(min_tracking_confidence=0.5, min_detection_confidence=0.5)

    # Variáveis de estado
    time_init1 = 0
    time_init2 = 0
    contador1 = 0
    contador2 = 0
    check1 = True
    check2 = True
    winner = False
    time_winner_player = 0

    while True:
        success, img = video.read()
        if not success:
            print("⚠️ Erro ao ler frame do vídeo.")
            break

        window_w, window_h = windowCurrentSize(window)
        img = cv2.resize(img, (window_w, window_h))

        if game_mode == 1:
            img, pose_detect1, contador1, draw, winner, time_init1, check1 = processPlayers(img, pose_module, pose_detect1, draw, contador1, 1, time_init1, check1)

        elif game_mode == 2:
            meio = window_w // 2
            img_esq = img[:, :meio].copy()
            img_dir = img[:, meio:].copy()

            img_esq, pose_detect1, contador1, draw, winner1, time_init1, check1 = processPlayers(img_esq, pose_module, pose_detect1, draw, contador1, 1, time_init1, check1)

            img_dir, pose_detect2, contador2, draw, winner2, time_init2, check2 = processPlayers(img_dir, pose_module, pose_detect2, draw, contador2, 2, time_init2, check2)


            # Junta as metades novamente
            img = cv2.hconcat([img_esq, img_dir])
            cv2.line(img, (meio, 0), (meio, window_h), LINE_COLOR_WITH, THICKNESS_LINE)
            winner = winner1 or winner2

        # Exibir imagem na janela
        cv2.imshow(window, img)

        if winner and time_winner_player == 0:
            time_winner_player = time.time()


        # print((time.time() - time_winner_player) >= TIME_WINNER)
        # print(time.time() - time_winner_player)
        # Tecla ESC ou tempo após vitória
        key = cv2.waitKey(20) & 0xFF
        if key == 27 or (winner and ((time.time() - time_winner_player) >= TIME_WINNER)):
            print("🔙 Voltando para a tela inicial...")
            contador1 = contador2 = 0
            UI.home_screen(video, window)
            break
