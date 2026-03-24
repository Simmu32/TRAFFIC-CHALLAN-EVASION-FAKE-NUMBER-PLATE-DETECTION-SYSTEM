import re

def is_valid_plate(plate):
    """
    Validates Indian number plate format:
    Format: XX00XX0000 (Example: DL01AB1234)
    """

    # Define regex pattern
    pattern = r"^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}$"

    # Match pattern
    if re.match(pattern, plate):
        return True
    else:
        return False


# Test cases (run this file directly)
if __name__ == "__main__":
    test_plates = [
        "DL01AB1234",  # valid
        "DL1AB1234",   # invalid
        "XX00XX0000",  # valid
        "DL01A1234",   # invalid
        "DL01AB12O4"   # invalid (O instead of 0)
    ]

    for plate in test_plates:
        print(f"{plate} -> {is_valid_plate(plate)}")