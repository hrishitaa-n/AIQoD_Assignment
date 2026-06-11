import os
import logging
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
CSV_PATH = "sample_data.csv"
OUTPUT_DIR = "output"
QUERIES_LOG = "Queries_generated.txt"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

log = logging.getLogger(__name__)