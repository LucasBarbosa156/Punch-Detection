import cv2
import numpy as np

from Fight_functions.config import (
    video_path, frame_width, frame_height,
    MODEL_PATH, cor_l1, cor_l2
)
from Fight_functions.detector import Detector
from Fight_functions.fighters import novo_lutador, processar_lutador
from Fight_functions.drawing import (
    desenhar_esqueleto, desenhar_trilha,
    desenhar_flash, desenhar_placar
)
from Fight_functions.champion import determinar_vencedor, exibir_tela_campeao

detector = Detector(MODEL_PATH)
lutadores = {1: novo_lutador(), 2: novo_lutador()}

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Erro: não foi possível abrir o vídeo em '{video_path}'.")
    exit()

cv2.namedWindow("Arbitro Virtual", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Arbitro Virtual", frame_width, frame_height)

while True:
    ret, frame = cap.read()

    if not ret:
        p1 = lutadores[1]["pontos"]
        p2 = lutadores[2]["pontos"]
        vencedor, cor_vencedor = determinar_vencedor(p1, p2)
        exibir_tela_campeao(frame_anterior, vencedor,
                            cor_vencedor, p1, p2, w, h)
        break

    frame = cv2.resize(frame, (frame_width, frame_height))
    h, w = frame.shape[:2]
    frame_anterior = frame.copy()

    pessoas = detector.detectar(frame)

    # Processa cada lutador
    for idx, pessoa in enumerate(pessoas[:2]):
        lut_key = idx + 1
        lut = lutadores[lut_key]
        cor = cor_l1 if lut_key == 1 else cor_l2

        lut, pontos_arm = processar_lutador(lut, pessoa["kps"])

        desenhar_trilha(frame, lut["trilha_esq"], cor)
        desenhar_trilha(frame, lut["trilha_dir"], cor)
        desenhar_esqueleto(frame, pontos_arm, cor)

    # Flash de impacto
    for i, lut in enumerate(lutadores.values()):
        if lut["flash"] > 0:
            cor_flash = cor_l1 if i == 0 else cor_l2
            frame = desenhar_flash(frame, cor_flash)
            lut["flash"] -= 1

    desenhar_placar(frame, lutadores[1], lutadores[2], w)

    cv2.imshow("Arbitro Virtual", frame)

    if cv2.waitKey(1) & 0xFF == -1:
        break

cap.release()
cv2.destroyAllWindows()
