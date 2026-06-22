from cryptography.fernet import Fernet
from model_encryption.byte_operator import ByteOperator
import os, io
class ModelSecurity:
    @staticmethod
    def load_encrypted_model(model_name: str):
        cipher = Fernet(ByteOperator.byte_reading('secret.key'))
        file_path = os.path.join('weights', model_name)
        if os.path.exists(file_path):
            model_bytes = ByteOperator.byte_reading(file_path)
            clean_bytes = cipher.decrypt(model_bytes)
            return io.BytesIO(clean_bytes)
        else:
            return None