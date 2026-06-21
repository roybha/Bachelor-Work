from abc import ABC, abstractmethod
from PIL.Image import Image
from typing import List, Dict, Any

class IDetector(ABC):
    """
        Загальний інтерфейс, щоб у разі заміни YOLO на іншу архітектуру (Faster R-CNN),
        не довелося переписувати весь контролер.
    """
    @abstractmethod
    def load_model(self, weights_path: str):
        """Завантажуємо ваги вказаної моделі"""
        pass

    @abstractmethod
    def predict(self, image: Image, conf: float) -> List[Dict[str, Any]]:
        """
            Виконуємо обробку (інференс) моделлю
            Результат -  стандартизований список словників (bbox, class, confidence)
        """
        pass