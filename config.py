import os
from dotenv import load_dotenv
from common.logger import setup_logger

# Load env vars
load_dotenv()

logger = setup_logger("config")

REQUIRED_CONFIGS = [
    "DATABASE_URL",
    "ACCESS_TOKEN_EXPIRE_MINUTES"
]

# Check missing configs
missing = [key for key in REQUIRED_CONFIGS if not os.getenv(key)]

if missing:
    logger.warning(
        f"⚠️ Missing environment variable(s): {', '.join(missing)}. "
        "Please check your .env file."
    )

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")  # top secret: not in REQUIRED_CONFIGS
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))
    EMAIL_CONFIG = {
        "provider": os.getenv("EMAIL_PROVIDER", "smtp"),
        "smtp": {
            "username": os.getenv("SMTP_USERNAME"),
            "password": os.getenv("SMTP_PASSWORD"),
            "server": os.getenv("SMTP_SERVER"),
            "port": int(os.getenv("SMTP_PORT", 587)),
        },
        "sendgrid": {
            "api_key": os.getenv("SENDGRID_API_KEY"),
        }
    }
