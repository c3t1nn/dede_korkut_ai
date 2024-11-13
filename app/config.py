import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Uygulama konfigürasyonu
class Config:
    # Flask konfigürasyonu
    SECRET_KEY = 'dede_korkut_secret_key'
    DEBUG = True

    # API konfigürasyonu
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    
    # Cache konfigürasyonu
    CACHE_TIMEOUT = 300  # 5 dakika
    MAX_CACHE_SIZE = 100
    
    # API limit konfigürasyonu
    API_RATE_LIMIT = 15  # Dakikada 15 istek
    API_TOKEN_LIMIT = 30720
    MAX_OUTPUT_TOKENS = 2048

    # Loglama konfigürasyonu
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    LOG_FILE = 'logs/dede_korkut.log'
    
    # AI Model konfigürasyonu
    MODEL_CONFIG = {
        'temperature': 0.9,
        'top_p': 0.9,
        'top_k': 40,
    }

    # Hikaye konfigürasyonu
    MIN_STORY_LENGTH = 1000  # Minimum kelime sayısı