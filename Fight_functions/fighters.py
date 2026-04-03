import numpy as np
from collections import deque

from Fight_functions.config import (
    ombro_esq, cotovelo_esq, pulso_esq,
    ombro_dir, cotovelo_dir, pulso_dir,
    angulo_dobrado, angulo_estendido,
    min_confianca, duracao_flash,
    maxlen_historico, maxlen_trilha
)


# Retorna um dicionário com o estado inicial de um lutador.
def novo_lutador():

    return {
        "estado_esq": "repouso",
        "estado_dir": "repouso",
        "pontos":     0,
        "hist_esq":   deque(maxlen=maxlen_historico),
        "hist_dir":   deque(maxlen=maxlen_historico),
        "trilha_esq": deque(maxlen=maxlen_trilha),
        "trilha_dir": deque(maxlen=maxlen_trilha),
        "flash":      0,
    }


def calcular_angulo(a, b, c):

    # Calcula o ângulo formado por três pontos onde b é o vértice.

    # a — ponto proximal (ex: ombro)
    # b — vértice (ex: cotovelo)
    # c — ponto distal (ex: pulso)
    # Retorna o ângulo em graus (0 a 180).

    a, b, c = np.array(a), np.array(b), np.array(c)
    vetor_ba = a - b
    vetor_bc = c - b
    angulo = np.degrees(
        np.arctan2(vetor_bc[1], vetor_bc[0]) -
        np.arctan2(vetor_ba[1], vetor_ba[0])
    )
    angulo = abs(angulo)
    if angulo > 180:
        angulo = 360 - angulo
    return angulo


def extrair_ponto(kps, idx_kp):

    # Extrai coordenadas em pixels e confiança de um keypoint.
    # kps = tensor de keypoints da pessoa (17, 3)
    # idx_kp = índice do keypoint desejado

    x = int(kps[idx_kp][0].item())
    y = int(kps[idx_kp][1].item())
    conf = float(kps[idx_kp][2].item())
    return (x, y), conf


def atualizar_estado(angulo, estado_atual, pontos):
    '''''''''
    Transições válidas:
    qualquer → dobrado   (angulo < angulo_dobrado)
    dobrado  → estendido (angulo > angulo_estendido) → +1 ponto

    Retorna:
    novo_estado — estado atualizado
    pontos      — pontuação atualizada
    soco        — True se um soco foi detectado neste frame
    '''''''''

    soco = False
    if angulo < angulo_dobrado:
        novo_estado = "dobrado"
    elif angulo > angulo_estendido:
        if estado_atual == "dobrado":
            novo_estado = "estendido"
            pontos += 1
            soco = True
        else:
            novo_estado = estado_atual
    else:
        novo_estado = estado_atual
    return novo_estado, pontos, soco


def processar_lutador(lut, kps):

    # Processa um frame para um lutador: extrai keypoints, calcula
    # ângulos, atualiza a máquina de estados e as trilhas.

    (oe, conf_oe) = extrair_ponto(kps, ombro_esq)
    (ce, conf_ce) = extrair_ponto(kps, cotovelo_esq)
    (pe, conf_pe) = extrair_ponto(kps, pulso_esq)
    (od, conf_od) = extrair_ponto(kps, ombro_dir)
    (cd, conf_cd) = extrair_ponto(kps, cotovelo_dir)
    (pd, conf_pd) = extrair_ponto(kps, pulso_dir)

    vis_e = min(conf_oe, conf_ce, conf_pe)
    vis_d = min(conf_od, conf_cd, conf_pd)

    if vis_e >= min_confianca:
        lut["hist_esq"].append(calcular_angulo(oe, ce, pe))
    if vis_d >= min_confianca:
        lut["hist_dir"].append(calcular_angulo(od, cd, pd))

    ang_e = sum(lut["hist_esq"]) / \
        len(lut["hist_esq"]) if lut["hist_esq"] else 0
    ang_d = sum(lut["hist_dir"]) / \
        len(lut["hist_dir"]) if lut["hist_dir"] else 0

    lut["estado_esq"], lut["pontos"], soco_e = atualizar_estado(
        ang_e, lut["estado_esq"], lut["pontos"])
    lut["estado_dir"], lut["pontos"], soco_d = atualizar_estado(
        ang_d, lut["estado_dir"], lut["pontos"])

    if soco_e or soco_d:
        lut["flash"] = duracao_flash

    lut["trilha_esq"].append(pe)
    lut["trilha_dir"].append(pd)

    pontos_arm = {
        "ombro_e": oe, "cotovelo_e": ce, "pulso_e": pe,
        "ombro_d": od, "cotovelo_d": cd, "pulso_d": pd,
        "ang_e": ang_e, "ang_d": ang_d,
    }

    return lut, pontos_arm
