import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # ── Database ──────────────────────────────────────────────────────────────
    # PG_URL: set trên Render/production → dùng PostgreSQL Supabase
    # Nếu không có → tự build MySQL URL từ DB_* vars (local dev)
    PG_URL: Optional[str] = None

    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "shopvn_user"
    DB_PASSWORD: str = "shopvn_pass"
    DB_NAME: str = "ecommerce_db"

    # ── Supabase ──────────────────────────────────────────────────────────────
    SUPABASE_URL: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_STORAGE_BUCKET: str = "uploads"

    # ── JWT ───────────────────────────────────────────────────────────────────
    SECRET_KEY: str = "your-super-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── Payment ───────────────────────────────────────────────────────────────
    MOMO_ENDPOINT: str = "https://test-payment.momo.vn/v3/gateway/api/create"
    MOMO_PARTNER_CODE: str = ""
    MOMO_ACCESS_KEY: str = ""
    MOMO_SECRET_KEY: str = ""
    VNPAY_TMN_CODE: str = ""
    VNPAY_HASH_SECRET: str = ""
    VNPAY_URL: str = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"
    VNPAY_RETURN_URL: str = "http://localhost:3000/payment/vnpay-return"

    # ── Server ────────────────────────────────────────────────────────────────
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = int(os.environ.get("PORT", 8000))
    DEBUG: bool = False          # ← default False, local dev tự set True trong .env
    ENVIRONMENT: str = "production"
    FRONTEND_URL: str = "http://localhost:3000"
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    # ── Email ─────────────────────────────────────────────────────────────────
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SENDER_EMAIL: str = "noreply@ecommerce.com"

    # ── Upload ────────────────────────────────────────────────────────────────
    UPLOAD_FOLDER: str = "uploads"
    MAX_FILE_SIZE: int = 10485760

    # ── Redis ─────────────────────────────────────────────────────────────────
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0

    # ── Logging ───────────────────────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    @property
    def DATABASE_URL(self) -> str:
        """
        Production (Render): set PG_URL=postgresql+psycopg2://...
        Local dev (XAMPP):   set DB_HOST=localhost trong .env
        """
        if self.PG_URL:
            url = self.PG_URL
            # Đảm bảo dùng psycopg2 driver
            url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
            url = url.replace("postgres://", "postgresql+psycopg2://", 1)
            return url
        # Fallback MySQL local
        return "mysql+pymysql://{}:{}@{}:{}/{}".format(
            self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_PORT, self.DB_NAME
        )

    @property
    def ALLOWED_ORIGINS_LIST(self):
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
