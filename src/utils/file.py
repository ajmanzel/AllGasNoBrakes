import random
import os

IMAGE_DIR = "images/"

def save_file_to_server(filename, data):
    exists = os.path.exists(IMAGE_DIR)
    if not exists:
        os.makedirs(IMAGE_DIR)
    with open(f"{IMAGE_DIR}{filename}", 'wb') as f:
        f.write(data)

def get_server_filename(filename):
    file_type = filename[-4:]
    return str(random.randint(100000000000, 999999999999)) + file_type