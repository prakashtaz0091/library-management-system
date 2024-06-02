import re

def is_valid_phone_number(number):
    pattern = r'^9[78]\d{8}$'
    return bool(re.match(pattern, number))