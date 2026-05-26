import re

INDIAN_STATE_CODES = {
    'AP', 'AR', 'AS', 'BR', 'CG', 'DL', 'GA', 'GJ', 'HR', 'HP', 'JK', 'JH', 'KA', 'KL', 'MP', 'MH', 'MN', 'ML', 'MZ', 'NL', 'OD', 'PB', 'RJ', 'SK', 'TN', 'TS', 'TR', 'UK', 'UP', 'WB'
}

def validate_plate_format(plate):
    pattern = r'^([A-Z]{2})(\d{2})([A-Z]{1,2})(\d{4})$'
    match = re.match(pattern, plate.upper())
    if not match:
        return False
    state, district, series, number = match.groups()
    if state not in INDIAN_STATE_CODES:
        return False
    if not district.isdigit() or int(district) < 1 or int(district) > 99:
        return False
    if len(series) > 2:
        return False
    if not number.isdigit() or len(number) != 4:
        return False
    return True

def check_character_validity(plate):
    # Detect O vs 0, I vs 1
    plate_upper = plate.upper()
    if 'O' in plate_upper and '0' in plate_upper:
        return False, "Ambiguous O/0"
    if 'I' in plate_upper and '1' in plate_upper:
        return False, "Ambiguous I/1"
    return True, "Valid"

def validate_state_code(state):
    return state.upper() in INDIAN_STATE_CODES

def detect_common_fakes(plate):
    plate_upper = plate.upper()
    fakes = []
    if 'O0' in plate_upper or '0O' in plate_upper:
        fakes.append("O/0 substitution")
    if 'I1' in plate_upper or '1I' in plate_upper:
        fakes.append("I/1 substitution")
    if plate_upper.count(' ') > 1:
        fakes.append("Excessive spaces")
    return fakes