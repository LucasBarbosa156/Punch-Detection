from ultralytics import YOLO

# config.py — Configurações centralizadas do projeto
# Altere os valores aqui para ajustar o comportamento do sistema

video_path = "lutas_inputs/luta_5.mp4"
frame_width = 1280
frame_height = 720

MODEL_PATH = YOLO("yolo11m-pose.pt").to("cuda")

# Índices COCO dos keypoints utilizados

ombro_esq = 5
cotovelo_esq = 7
pulso_esq = 9
ombro_dir = 6
cotovelo_dir = 8
pulso_dir = 10

# Ajuste esses valores caso a detectação não funcione de maneira correta com seu input
# Observe os ângulos exibidos nos cotovelos durante a execução.

angulo_dobrado = 70    # abaixo disso = braço em guarda
angulo_estendido = 98    # acima disso = soco executado
min_confianca = 0.5   # confiança mínima do keypoint

duracao_flash = 4     # frames que o flash de impacto dura
maxlen_historico = 5     # janela de suavização dos ângulos
maxlen_trilha = 20    # comprimento da trilha do pulso

# Cores por lutador
cor_l1 = (255, 140, 0)
cor_l2 = (0, 80, 255)
