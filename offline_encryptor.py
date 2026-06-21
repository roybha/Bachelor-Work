from cryptography.fernet import Fernet
import os

def key_creation(secret_key: bytes):
    with open('secret.key', 'wb') as file:
        file.write(secret_key)

def read_model(file_path: str):
    with open(file_path, 'rb') as file:
        model_data = file.read()
    return model_data

def model_encryption(encrypted_model: bytes, output_path: str):
    with open(output_path, 'wb') as file:
        file.write(encrypted_model)
def get_model():
    key = Fernet.generate_key()
    key_creation(key)
    cipher = Fernet(key)
    for filename in os.listdir('weights'):
        if filename.endswith('.pt'):
            file_path = os.path.join('weights', filename)
            encrypted_model_data = cipher.encrypt(read_model(file_path))
            encrypted_file = file_path.replace('.pt','.enc')
            model_encryption(encrypted_model_data, encrypted_file)
get_model()