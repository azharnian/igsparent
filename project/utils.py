import uuid
import os

def generate_random_filename(instance, filename, directory):
    ext = filename.split('.')[-1]
    random_name = uuid.uuid4().hex
    return os.path.join(directory, f'{random_name}.{ext}')