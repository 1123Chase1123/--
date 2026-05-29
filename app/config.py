"""应用配置 —— 适配 PyInstaller 打包路径"""

import os
import sys


def _get_data_dir():
    """
    获取可写数据目录：
    - 开发模式：项目根目录
    - 打包 exe：exe 所在目录下的 _data/
    """
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), '_data')
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


DATA_DIR = _get_data_dir()

# 确保数据目录存在
_DB_DIR = os.path.join(DATA_DIR, 'database')
_UPLOAD_DIR = os.path.join(DATA_DIR, 'uploads')
os.makedirs(_DB_DIR, exist_ok=True)
os.makedirs(_UPLOAD_DIR, exist_ok=True)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # 数据库 —— SQLite，存在可写目录
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f'sqlite:///{os.path.join(DATA_DIR, "database", "study_review.db")}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 文件上传目录
    UPLOAD_FOLDER = os.path.join(DATA_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'md', 'doc', 'docx'}

    # Session
    SESSION_COOKIE_NAME = 'study_review_session'
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 7  # 7天

    # Flask-Login 记住我配置
    REMEMBER_COOKIE_NAME = 'study_review_remember'
    REMEMBER_COOKIE_DURATION = 60 * 60 * 24 * 7  # 7天
    REMEMBER_COOKIE_HTTPONLY = True
