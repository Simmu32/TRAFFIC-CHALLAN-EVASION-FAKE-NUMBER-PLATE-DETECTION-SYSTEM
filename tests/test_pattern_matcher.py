import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pattern_matcher as pm

def test_valid_plate():
    assert pm.validate_plate_format("MH12AB1234") == True
    assert pm.validate_plate_format("DL01C5678") == True

def test_invalid_plate():
    assert pm.validate_plate_format("XX99ZZ9999") == False
    assert pm.validate_plate_format("MH12AB123") == False

def test_fake_detection():
    fakes = pm.detect_common_fakes("MH0O1234")
    assert len(fakes) > 0