import cv2
from ultralytics import YOLO


class Detector:

    # Encapsula o modelo YOLOv11-pose e o rastreamento ByteTrack.
    # Detecta pessoas e retornar keypoints por frame
    # Ordena os lutadores da esquerda para a direita

    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detectar(self, frame):

        # Retorna lista de dicionários ordenada da esquerda para a direita:
        # id = ID do rastreador
        # x1 = borda esquerda da bounding box
        # kps = tensor de keypoints (17, 3): x, y, confiança

        resultados = self.model.track(
            frame,
            persist=True,
            classes=[0],
            verbose=False
        )

        pessoas = []

        if resultados[0].boxes is None or resultados[0].keypoints is None:
            return pessoas

        for i, box in enumerate(resultados[0].boxes):
            track_id = int(box.id[0]) if box.id is not None else -1
            x1 = int(box.xyxy[0][0].item())
            kps = resultados[0].keypoints.data[i]

            pessoas.append({
                "id":  track_id,
                "x1":  x1,
                "kps": kps,
            })

        # Ordena da esquerda para a direita — L1 = mais à esquerda
        pessoas.sort(key=lambda p: p["x1"])
        return pessoas
