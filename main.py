import os
from app.services.detector_service import YOLOInferenceService
from app.utils.image_processor import ImageProcessor
from app.routers.detect import DetectionController
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request


class AppBuilder:
    """
        Використано паттерн програмування будівельник(Builder) для налаштування FastAPI додатку
        Уникаючи створення глобальних змінних та акуратно ініціалізувати всі сервіси
    """
    def __init__(self):
        self.app = FastAPI(
            title="YOLO Detection OOP API",
            version="1.0.0",
            description="Backend for YOLO inference"
        )
        # Використовуємо Jinja2 для рендеру базових HTML-сторінок
        self.templates = Jinja2Templates(directory="templates")

        # Викликаємо методи налаштування

        # Створення сервісів для роботи YOLO, преобробки зображення
        # + створення контролера, що буде керувати даними сервісами
        self._setup_dependencies()

        # Підключення маршрутизатора, зсередини створеного контролера
        self._setup_routes()

        # Налаштування статичних файлів (js/css)
        self._setup_statics()

    def _setup_dependencies(self):
        # Спочатку створюємо базові сервіси (робота з моделлю та зображеннями),
        # а потім передаємо їх у контролер
        self.detector_service = YOLOInferenceService()
        self.image_service = ImageProcessor()
        self.detection_controller = DetectionController(self.detector_service, self.image_service)

    def _setup_routes(self):
        # Підключаємо маршрути з нашого контролера
        # для коретктної детекції об'єктів
        self.app.include_router(self.detection_controller.router)

        @self.app.get("/")
        # Головна сторінка для роботи
        async def index(request: Request):
            return self.templates.TemplateResponse("index.html", {"request": request})

        @self.app.get("/models")
        # Динамічно зчитуємо доступні моделі з папки weights, без перезапуску серверу
        async def get_models():
            models_dir = "weights"
            if not os.path.exists(models_dir):
                return []
            return [file for file in os.listdir(models_dir) if file.endswith(".pt")]

    def _setup_statics(self):
        # Вказуємо статичні (css/js)
        self.app.mount("/static", StaticFiles(directory="static"), name="static")

    def get_app(self) -> FastAPI:
        return self.app


# Точка входу програми (Uvicorn)
app = AppBuilder().get_app()