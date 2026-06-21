import io
import base64
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Any


class ImageProcessor:
    """
        Клас для роботи з зображеннями
        Інкапсулює в собі всю логіку малювання рамок та конвертації форматів
    """
    def __init__(self, default_font: str = "arial.ttf"):
        self.default_font = default_font

    def decode_image(self, image_bytes: bytes) -> Image.Image:
        """Перетворює байти з HTTP-запиту в об'єкт Image"""
        return Image.open(io.BytesIO(image_bytes)).convert("RGB")

    def draw_bounding_boxes(self, image: Image.Image, detections: List[Dict[str, Any]]) -> Image.Image:
        """Метод, що малює рамки та підписи класів на зображенні"""
        draw = ImageDraw.Draw(image)
        width, height = image.size

        # Динамічно розраховуємо товщину ліній і розмір шрифту залежно від розміру картинки,
        # щоб рамки не були занадто товстими на маленьких фото і навпаки
        line_width = max(1, int(min(width, height) * 0.005))
        font_size = max(12, int(min(width, height) * 0.02))

        try:
            font = ImageFont.truetype(self.default_font, font_size)
        except IOError:
            font = ImageFont.load_default()

        for detection in detections:
            # Отримуємо координати рамки об'єкта
            x1, y1, x2, y2 = detection['bbox']

            # Отримуємо підпис класу
            label = f"{detection['class_name']} {detection['confidence']:.2f}"

            # Малюємо саму рамку по заданих координатах
            draw.rectangle([(x1, y1), (x2, y2)], outline='red', width=line_width)

            # Робимо плашку для тексту, щоб він добре читався
            text_bbox = draw.textbbox((x1, y1), label, font=font)
            padding = int(font_size * 0.2)
            draw.rectangle(
                (text_bbox[0], text_bbox[1], text_bbox[2] + padding, text_bbox[3] + padding),
                fill='red'
            )

            # Виводимо текст поверх плашки
            draw.text((x1 + padding // 2, y1), label, fill='white', font=font)

        return image

    def encode_to_base64(self, image: Image.Image) -> str:
        """Кодує PIL Image у рядок Base64, щоб його можна було передати у JSON"""
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")