import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.adzuna.com/v1/api"
SEARCH_URL = "/jobs/gb/search/"
QUERY = "junior data engineer"
RESULTS_PER_PAGE = 50

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getev("DB_USER"),
    "password": os.getev("DB_PASSWORD"),
}