class ByteOperator:
    @staticmethod
    def byte_record(out_file: str, data: bytes):
        with open(out_file, 'wb') as file:
            file.write(data)

    @staticmethod
    def byte_reading(file_path: str):
        with open(file_path, 'rb') as file:
            file_bytes_data = file.read()
        return file_bytes_data