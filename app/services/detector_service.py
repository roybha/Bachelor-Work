from ultralytics import YOLO
from app.utils.logger import logger
from app.services.detector_interface import IDetector
from PIL.Image import Image
from typing import List, Dict, Any


class YOLOInferenceService(IDetector):
    """
        Реалізація інтрфйесу IDetector для роботи з YOLO
    """
    def __init__(self, weights_path: str = None):
        self.model = None
        self.current_model_name = None

        # Завантажуємо модель, якщо передано конкретний шлях
        if weights_path:
            self.load_model(weights_path)

    def load_model(self, weights_path: str) -> None:
        # Якщо модель вже є в пам'яті - не завантажуємо її повторно
        if self.current_model_name == weights_path and self.model is not None:
            logger.info(f"Model {weights_path} already loaded.")
            return

        logger.info(f"Loading model: {weights_path}...")
        try:
            # Пробуємо встановити модель, для інференсу
            self.model = YOLO(weights_path)
            self.current_model_name = weights_path
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise e

    def predict(self, image: Image, conf: float = 0.25) -> List[Dict[str, Any]]:
        # Перевіряємо чи взагалі завантажена модель
        if self.model is None:
            logger.warning("Attempt to predict without loaded model!")
            raise ValueError("Model not loaded yet")

        # Починаємо процес інференсу для обраної моделі
        logger.info(f"Starting inference with conf={conf}")
        # Викликаємо метод, що безпосередньо займається передбаченням
        results = self.model.predict(image, conf=conf)
        detections = []

        result = results[0] if isinstance(results, list) else results

        # Конвертуємо результати і переводимо у формат словника
        if result.boxes is not None:
            for box in result.boxes:
                # Беремо координати рамки (xyxy формат)
                x1, y1, x2, y2 = box.xyxy[0].tolist()

                # Беремо значення впевненості моделі у приналежності об'єкта
                confidence = box.conf[0].item()

                # Беремо клас виявленого об'єкта
                cls_id = int(box.cls[0].item())

                # Визначаємо підпис для знайденого представника класу
                label = result.names[cls_id]

                # Записуємо значення у список словників
                detections.append({
                    "class_name": label,
                    "confidence": confidence,
                    "bbox": [x1, y1, x2, y2]
                })
        return detections