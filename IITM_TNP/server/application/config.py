class Config():
    SQLALCHEMY_DATABASE_URI = "sqlite:///tnpdb.sqlite3"
    SECRET_KEY =  "top secret"
    JWT_SECRET_KEY = 'your_jwt_secret_key_here'
    #celery config
    REDIS_URL = "redis://localhost:6379"
    CELERY_BROKER_URL="redis://localhost:6379"
    CELERY_RESULT_BACKEND= "redis://localhost:6379"
    ENABLE_UTC = False
    TIMEZONE = "Asia/Calcutta"
