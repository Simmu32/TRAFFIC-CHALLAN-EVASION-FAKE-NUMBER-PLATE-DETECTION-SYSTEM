import json
import logging
from functools import wraps
from flask import jsonify, request
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def response_formatter(success, data=None, message=None, error=None):
    return {
        "success": success,
        "data": data,
        "message": message,
        "error": error
    }

def validate_input(required_fields):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            data = request.get_json(silent=True) or {}
            missing = [field for field in required_fields if field not in data]
            if missing:
                return jsonify(response_formatter(False, error=f"Missing fields: {missing}")), 400
            return f(*args, **kwargs)
        return wrapped
    return decorator

def export_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    logger.info(f"Exported {len(data)} rows to {filename}")