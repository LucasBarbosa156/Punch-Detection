import cv2

from Fight_functions.config import cor_l1, cor_l2


def desenhar_esqueleto(frame, pontos_arm, cor):

    # Desenha os keypoints e conexões dos braços no frame.
    # pontos_arm — dicionário com coordenadas dos pontos

    oe = pontos_arm["ombro_e"]
    ce = pontos_arm["cotovelo_e"]
    pe = pontos_arm["pulso_e"]
    od = pontos_arm["ombro_d"]
    cd = pontos_arm["cotovelo_d"]
    pd = pontos_arm["pulso_d"]

    for p in [oe, ce, pe, od, cd, pd]:
        cv2.circle(frame, p, 6, cor, -1)

    for pa, pb in [(oe, ce), (ce, pe), (od, cd), (cd, pd), (oe, od)]:
        cv2.line(frame, pa, pb, cor, 3)

    # Ângulos ao lado dos cotovelos
    cv2.putText(frame, f"{pontos_arm['ang_e']:.0f}", ce,
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, cor, 2)
    cv2.putText(frame, f"{pontos_arm['ang_d']:.0f}", cd,
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, cor, 2)


# Desenha a trilha de movimento do pulso
def desenhar_trilha(frame, trilha, cor):

    pontos = list(trilha)
    for i in range(1, len(pontos)):
        if pontos[i - 1] is None or pontos[i] is None:
            continue
        alpha = i / len(pontos)
        espessura = max(1, int(4 * alpha))
        cor_fade = tuple(int(c * alpha) for c in cor)
        cv2.line(frame, pontos[i - 1], pontos[i], cor_fade, espessura)


def desenhar_flash(frame, cor, intensidade=0.35):
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), cor, -1)
    return cv2.addWeighted(overlay, intensidade, frame, 1 - intensidade, 0)


def desenhar_placar(frame, l1, l2, largura):

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (largura, 70), (20, 20, 20), -1)
    frame[:] = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)

    cv2.putText(frame, "AZUL", (40, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor_l1, 2)
    cv2.putText(frame, str(l1["pontos"]), (40, 62),
                cv2.FONT_HERSHEY_SIMPLEX, 1.4, cor_l1, 3)

    cv2.line(frame, (largura // 2, 8), (largura // 2, 62), (100, 100, 100), 1)
    cv2.putText(frame, "VS", (largura // 2 - 18, 44),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (180, 180, 180), 2)

    cv2.putText(frame, "VERMELHO", (largura - 220, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor_l2, 2)
    cv2.putText(frame, str(l2["pontos"]), (largura - 80, 62),
                cv2.FONT_HERSHEY_SIMPLEX, 1.4, cor_l2, 3)
