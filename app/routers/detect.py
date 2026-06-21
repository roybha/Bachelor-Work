import os
import time
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.detector_interface import IDetector
from app.utils.image_processor import ImageProcessor
from app.schemas.response import DetectionResponse


class DetectionController:
    """
        Клас, що керує HTTP-запитами, що стосуються детекції
        Використовуємо впроваджені залежності (detector та image_processor),
        щоб не створювати їх всередині методів.
    """
    def __init__(self, detector: IDetector, image_processor: ImageProcessor):
        # Контролер приймає залежності через конструктор
        self.detector = detector
        self.image_processor = image_processor
        self.router = APIRouter(prefix="/detect", tags=["Detection"])

        # Реєструємо маршрути при створенні об'єкта
        self._register_routes()

    def _register_routes(self):
        @self.router.post("/annotated_data" ,response_model=DetectionResponse)
        # Маршрут обробки завантаженого файлу обраною моделлю
        # із певним порогом впевненості
        async def detect_objects(
                file: UploadFile = File(...),
                model_name: str = Form(...),
                confidence: float = Form(0.25)
        ):
            # Делегуємо основну логіку окремому методу
            return await self.handle_detection(file, model_name, confidence)

    async def handle_detection(self, file: UploadFile, model_name: str, confidence: float) -> DetectionResponse:
        weights_path = os.path.join("weights", model_name)

        # Перевіряємо чи існує файл з вагами моделі
        if not os.path.exists(weights_path):
            raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found")

        # 1. Завантаження ваг моделі
        self.detector.load_model(weights_path)

        # 2. Зчитуємо байти і декодувємо зображення у формат Image
        image_bytes = await file.read()
        image = self.image_processor.decode_image(image_bytes)

        # 3. Виконуємо інференс і заміряємо час виконання
        start_time = time.time()
        detections = self.detector.predict(image, conf=confidence)
        inference_time = round((time.time() - start_time) * 1000, 2)

        # 4. Малюємо рамки на картинці та перетворюємо її в base64 для відправки назад
        annotated_image = self.image_processor.draw_bounding_boxes(image, detections)
        base64_img = self.image_processor.encode_to_base64(annotated_image)

        # 5. Повернення фінального результату
        return DetectionResponse(
            objects=detections,
            image_base64=base64_img,
            inference_time=inference_time,
            object_count=len(detections)
        )