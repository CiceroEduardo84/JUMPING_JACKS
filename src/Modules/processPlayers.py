import cv2
import math
import time

from Modules.checkfacingforward import checkfacingforward
from Config.variablesConfig import MAX_TIME_MOVEMENT, MAX_JUMPING_JACKS, DIFFICULTY
from Style.varScreens import ESPESSURA_TEXTO_MSG_HOME, TAMANHO_FONTE_MSG_HOME, TEXT_COLOR_YELLOW
from Style.varPlayers import (
    PLAYER_COLOR1,
    PLAYER_COLOR2,
    PLAYER_CONFIG_COLOR1,
    PLAYER_CONFIG_COLOR2,
    PLAYERS_CONFIG_LINES,
    TEXT_COLOR_RED,
    TEXT_COLOR_WHITE,
    TEXT_SIZE_CAUNT,
    TEXT_SCALE_COUNT,
    TEXT_STYLE_CAUNT
)


def processPlayers(img, pose_module, pose_detect, draw, contador, id_player, time_init, check):
    winner = False
    h, w = img.shape[:2]

    # Escolhe cor conforme jogador
    player_color = PLAYER_COLOR1 if id_player == 1 else PLAYER_COLOR2
    player_config_color = PLAYER_CONFIG_COLOR1 if id_player == 1 else PLAYER_CONFIG_COLOR2

    # Processa pose
    videoRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose_detect.process(videoRGB)
    points = results.pose_landmarks

    # Escala para texto
    escala = TAMANHO_FONTE_MSG_HOME / 2 * (h / 600)
    espessura = max(1, int(ESPESSURA_TEXTO_MSG_HOME * escala))

    if points:
        # Desenha esqueleto
        draw.draw_landmarks(
            img, points, pose_module.POSE_CONNECTIONS,
            landmark_drawing_spec=player_config_color,
            connection_drawing_spec=PLAYERS_CONFIG_LINES
        )

        # Verifica se o jogador está de frente
        facing = checkfacingforward(points, pose_module)
        if not facing:
            msg_turn = "Vire de frente!"
            (tw, th), _ = cv2.getTextSize(msg_turn, cv2.FONT_HERSHEY_TRIPLEX, escala, espessura)
            px = (w - tw) // 2
            py = (h + th) // 2
            cv2.putText(img, msg_turn, (px, py), TEXT_STYLE_CAUNT, TEXT_SCALE_COUNT, TEXT_COLOR_RED, TEXT_SIZE_CAUNT)

        # Coordenadas
        peD = points.landmark[pose_module.PoseLandmark.RIGHT_FOOT_INDEX]
        peE = points.landmark[pose_module.PoseLandmark.LEFT_FOOT_INDEX]
        maoD = points.landmark[pose_module.PoseLandmark.RIGHT_INDEX]
        maoE = points.landmark[pose_module.PoseLandmark.LEFT_INDEX]

        peD_X, peD_Y = int(peD.x * w), int(peD.y * h)
        peE_X, peE_Y = int(peE.x * w), int(peE.y * h)
        maoD_X, maoD_Y = int(maoD.x * w), int(maoD.y * h)
        maoE_X, maoE_Y = int(maoE.x * w), int(maoE.y * h)

        # Distâncias
        distMaos = math.hypot(maoD_X - maoE_X, maoD_Y - maoE_Y)
        distPes = math.hypot(peD_X - peE_X, peD_Y - peE_Y)

        msg_sleep = "Mais rápido!"

        if not check and distMaos >= DIFFICULTY and distPes >= DIFFICULTY and facing:
            check = True
            time_init = time.time()

        # Se jogador fechar (mãos e pés próximos), conta 1
        elif check and distMaos <= DIFFICULTY and distPes <= DIFFICULTY and facing:
            time_finally = time.time()
            time_movement = time_finally - time_init

            if 0 < time_movement <= MAX_TIME_MOVEMENT:
                contador += 1
                msg_sleep = ""
            else:
                (tw, th), _ = cv2.getTextSize(msg_sleep, cv2.FONT_HERSHEY_TRIPLEX, escala, espessura)
                px = (w - tw) // 2
                py = (h + th) // 2
                cv2.putText(img, msg_sleep, (px, py), TEXT_STYLE_CAUNT, TEXT_SCALE_COUNT, TEXT_COLOR_RED, TEXT_SIZE_CAUNT)

            check = False
            
        # --- CONDIÇÃO DE VITÓRIA ---
        if contador >= MAX_JUMPING_JACKS:
            msg_winner = f"Jogador {id_player} venceu!"
            (tw, th), _ = cv2.getTextSize(msg_winner, cv2.FONT_HERSHEY_TRIPLEX, escala, espessura)
            px = (w - tw) // 2
            py = (h + th) // 2
            cv2.putText(img, msg_winner, (px, py), TEXT_STYLE_CAUNT, TEXT_SCALE_COUNT, TEXT_COLOR_YELLOW, TEXT_SIZE_CAUNT)
            winner = True

        # --- CONTADOR VISUAL ---
        texto = f'Player {id_player}: {contador}'
        cv2.rectangle(img, (0, 0), (185, 50), player_color, -1)
        cv2.putText(img, texto, (10, 35), TEXT_STYLE_CAUNT, TEXT_SCALE_COUNT, TEXT_COLOR_WHITE, TEXT_SIZE_CAUNT)

    else:
        # Nenhum jogador visível
        msg_turn = "Aguardando jogador..."
        (tw, th), _ = cv2.getTextSize(msg_turn, cv2.FONT_HERSHEY_DUPLEX, escala * 0.7, espessura)
        px = (w - tw) // 2
        py = (h + th) // 2
        cv2.putText(img, msg_turn, (px, py), TEXT_STYLE_CAUNT, TEXT_SCALE_COUNT * 0.7, TEXT_COLOR_YELLOW, TEXT_SIZE_CAUNT)

    # Retorna os valores atualizados
    return img, pose_detect, contador, draw, winner, time_init, check
