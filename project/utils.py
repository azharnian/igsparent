import uuid
import os
import re

from django.core.exceptions import ValidationError

def generate_random_filename(instance, filename, directory):
    ext = filename.split('.')[-1]
    random_name = uuid.uuid4().hex
    return os.path.join(directory, f'{random_name}.{ext}')

def validate_url(value):
    pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or IPv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or IPv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if not re.match(pattern, value):
        raise ValidationError("Invalid URL")
