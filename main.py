import os
from app.services.detector_service import YOLOInferenceService
from app.utils.image_processor import ImageProcessor
from app.routers.detect import DetectionController
from model_encryption.security import ModelSecurity
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request


class AppBuilder:
    default_model = "yolo11n_ep150_img640_augY_v2_best.enc"
    """
        Використано паттерн програмування будівельник(Builder) для налаштування FastAPI додатку
        Уникаючи створення глобальних змінних та акуратно ініціалізувати всі сервіси
    """
    def __init__(self):
        self.app = FastAPI(
            title="YOLO Detection OOP API",
            version="1.0.0",
            description="Backend for YOLO inference",
            lifespan=self.app_lifespan
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
        self.detection_controller = DetectionController(YOLOInferenceService(), ImageProcessor())

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
            return [file for file in os.listdir(models_dir) if file.endswith(".enc")]

        @self.app.post("/switch_model")
        async def switch_model(model_name: str):
            if model_name == self.app.state.current_active_model:
                return {"status": "success", "message":"Model is already active"}
            result = ModelSecurity.load_encrypted_model(model_name)
            if result is None:
                return {"status": "error", "message":"Model not found"}
            (self.detection_controller.
             detector.load_model(result, model_name))
            self.app.state.current_active_model = model_name
            return {"status": "success", "active_model":f"{model_name}"}

    def _setup_statics(self):
        # Вказуємо статичні (css/js)
        self.app.mount("/static", StaticFiles(directory="static"), name="static")

    def get_app(self) -> FastAPI:
        return self.app

    @asynccontextmanager
    async def app_lifespan(self, app: FastAPI):
        clean_model = ModelSecurity.load_encrypted_model(self.default_model)
        (self.detection_controller.
         detector.load_model(clean_model, self.default_model)
         )
        app.state.current_active_model = self.default_model # type: ignore
        yield

# Точка входу програми (Uvicorn)
app = AppBuilder().get_app()