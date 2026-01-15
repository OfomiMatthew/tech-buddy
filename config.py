import os
from datetime import timedelta

class Config:
    # Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database config
    SQLALCHEMY_DATABASE_URI = 'sqlite:///techbuddy.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload config
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static/uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size for multimedia
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp3', 'wav', 'ogg', 'mp4', 'webm', 'pdf', 'doc', 'docx', 'txt', 'zip'}
    
    # Session config
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Pagination
    USERS_PER_PAGE = 20
    MESSAGES_PER_PAGE = 50
    
    # Age restriction
    MIN_AGE = 18
    MAX_AGE = 100
    
    # Groq API config
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY') or 'gsk_REPLACE_WITH_YOUR_KEY'
    GROQ_MODEL = 'llama-3.3-70b-versatile'  # Fast and powerful model
