from pydantic import BaseModel
from  typing import List

class Detection(BaseModel):
    class_name: str
    confidence: float
    bbox: List[float]

class DetectionResponse(BaseModel):
    objects : List[Detection]
    inference_time: float
    object_count: int
    image_base64: str