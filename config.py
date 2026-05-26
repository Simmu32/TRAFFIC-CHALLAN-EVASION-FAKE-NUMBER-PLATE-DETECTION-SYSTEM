import os

class Config:
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'traffic_system.db')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-prod')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')