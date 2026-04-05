import re

def is_valid_plate(plate):
    pattern = r"^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}$"
    return bool(re.match(pattern, plate))
