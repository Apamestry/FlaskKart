import os
from dotenv import load_dotenv

# Loads variables from a .env file in the project root into the environment.
load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def validate():
        """Fail loudly at startup instead of silently connecting with None values."""
        required = ["SECRET_KEY", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
        missing = [name for name in required if not os.getenv(name)]
        if missing:
            raise RuntimeError(
                f"Missing required environment variables: {', '.join(missing)}. "
                "Did you create a .env file? See .env.example."
            )