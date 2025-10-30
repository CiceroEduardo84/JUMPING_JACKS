import cv2
from Style.varScreens import ESPESSURA_TEXTO_MSG_HOME, TAMANHO_FONTE_MSG_HOME, TEXT_COLOR_YELLOW

from Modules.windowCurrentSize import windowCurrentSize
from UI.game import game_player

def home_screen(video, window):
    if not video.isOpened():
        print("❌ Erro: não foi possível abrir a câmera.")
        return

    # Pega tamanho inicial da janela
    prev_w, prev_h = 0, 0

    while True:
        ret, frame = video.read()
        if not ret:
            continue

        # Descobre o tamanho atual da janela
        window_w, window_h = windowCurrentSize(window)

        # Verifica se o tamanho é zero caso seja ignora e pega no proximo frame
        if window_w <= 0 or window_h <= 0:
            continue

        # Se o tamanho mudou (maximizou, restaurou, ou redimensionou)
        if (window_w != prev_w) or (window_h != prev_h):
            prev_w, prev_h = window_w, window_h

        # Redimensiona o frame conforme o tamanho da janela
        frame = cv2.resize(frame, (window_w, window_h))

        h, w = frame.shape[:2]
        msg = "Numero de jogadores: 1 ou 2?"
        escala = TAMANHO_FONTE_MSG_HOME / 2 * (h / 600)
        espessura = max(1, int(ESPESSURA_TEXTO_MSG_HOME * escala))
        (tw, th), _ = cv2.getTextSize(msg, cv2.FONT_HERSHEY_TRIPLEX, escala, espessura)
        px = (w - tw) // 2
        py = h // 2 + th // 2

        tela = frame * 0
        cv2.putText(tela, msg, (px, py), cv2.FONT_HERSHEY_TRIPLEX, escala, TEXT_COLOR_YELLOW, espessura)

        cv2.imshow(window, tela)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('1'):
            game_player(video,window, 1, w, h)
            break
        elif key == ord('2'):
            game_player(video, window, 2, w, h)
            break
        elif key == 27:  # ES
            break
