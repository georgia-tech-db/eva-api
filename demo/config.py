import pathlib
import os

FLASK_HOST="0.0.0.0"
FLASK_PORT=5001

DATASET_DIR = pathlib.Path().absolute() / 'dataset'
EVA_HOST = os.getenv('EVA_HOSTNAME')
EVA_PORT = int(os.getenv('EVA_PORT'))
