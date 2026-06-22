from cryptography.fernet import Fernet
from model_encryption.byte_operator import ByteOperator
import os

def create_encrypted_model():
    key = Fernet.generate_key()
    ByteOperator.byte_record('..secret.key',key)
    cipher = Fernet(key)
    for filename in os.listdir('../weights'):
        if filename.endswith('.pt'):
            file_path = os.path.join('../weights', filename)
            encrypted_model_data = cipher.encrypt(ByteOperator.byte_reading(file_path))
            encrypted_model_file = file_path.replace('.pt','.enc')
            ByteOperator.byte_record(encrypted_model_file, encrypted_model_data)


if __name__ == '__main__':
    create_encrypted_model()