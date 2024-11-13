from flask import Flask
import logging
import os
from .config import Config

# Flask uygulamasını oluştur
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

app = Flask(__name__, 
           template_folder=template_dir,
           static_folder=static_dir)

# Konfigürasyon ayarlarını yükle
app.config.from_object(Config)

# Loglama ayarlarını yapılandır
logging.basicConfig(
    level=logging.INFO,
    format=Config.LOG_FORMAT,
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)

# Route'ları içe aktar
from . import routes