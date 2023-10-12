from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Assign variables
MONGO_URI = os.getenv("MONGO_URI")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
