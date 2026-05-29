"""考研知识点复习系统 —— Flask 应用工厂"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(testing=False):
    app = Flask(__name__)

    # 配置
    from app.config import Config
    app.config.from_object(Config)
    if testing:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)

    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.notes import notes_bp
    from app.routes.review import review_bp
    from app.routes.statistics import statistics_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(notes_bp, url_prefix='/notes')
    app.register_blueprint(review_bp, url_prefix='/review')
    app.register_blueprint(statistics_bp, url_prefix='/statistics')

    # 模板上下文处理器
    @app.context_processor
    def inject_globals():
        from datetime import datetime
        return {'now': datetime.utcnow}

    # 首页重定向
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('auth.login'))

    # 创建数据库表
    with app.app_context():
        from app.models import user, note, tag, review_plan  # noqa: F401
        db.create_all()

    return app
