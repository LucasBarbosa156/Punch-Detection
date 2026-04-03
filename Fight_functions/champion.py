import cv2

from Fight_functions.config import cor_l1, cor_l2


def determinar_vencedor(pontos_l1, pontos_l2):

    if pontos_l1 > pontos_l2:
        return "AZUL", cor_l1
    elif pontos_l2 > pontos_l1:
        return "VERMELHO", cor_l2
    else:
        return "EMPATE", (200, 200, 200)


def exibir_tela_campeao(frame_base, vencedor, cor_vencedor, p1, p2, w, h):

    while True:
        tela = frame_base.copy()

        # Fundo escuro semitransparente
        overlay = tela.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 0), -1)
        tela = cv2.addWeighted(overlay, 0.65, tela, 0.35, 0)

        # Faixa central colorida
        cy = h // 2
        overlay2 = tela.copy()
        cv2.rectangle(overlay2, (0, cy - 100), (w, cy + 100), cor_vencedor, -1)
        tela = cv2.addWeighted(overlay2, 0.4, tela, 0.6, 0)

        # Texto CAMPEAO!
        texto_camp = "CAMPEAO!"
        (larg, _), _ = cv2.getTextSize(
            texto_camp, cv2.FONT_HERSHEY_SIMPLEX, 2.5, 4)
        cv2.putText(tela, texto_camp, ((w - larg) // 2, cy - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 4)

        # Texto LUTADOR X ou EMPATE
        texto_lut = f"LUTADOR {vencedor}" if vencedor != "EMPATE" else "EMPATE!"
        (larg2, _), _ = cv2.getTextSize(
            texto_lut, cv2.FONT_HERSHEY_SIMPLEX, 1.4, 3)
        cv2.putText(tela, texto_lut, ((w - larg2) // 2, cy + 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255, 255, 255), 3)

        # Placar final
        texto_placar = f"Azul {p1}  x  {p2} Vermelho"
        (larg3, _), _ = cv2.getTextSize(
            texto_placar, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)
        cv2.putText(tela, texto_placar, ((w - larg3) // 2, cy + 140),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (200, 200, 200), 2)

        # Instrução de saída
        cv2.putText(tela, "pressione qualquer tecla para sair",
                    (w // 2 - 220, h - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)

        cv2.imshow("Arbitro Virtual", tela)

        if cv2.waitKey(100) != -1:
            break
