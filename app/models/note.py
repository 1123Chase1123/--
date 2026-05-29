"""知识点模型"""

from datetime import datetime
from app import db


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    subject = db.Column(db.String(100), nullable=False, index=True)       # 科目
    chapter = db.Column(db.String(200), nullable=True)                     # 章节
    title = db.Column(db.String(200), nullable=False)                      # 标题
    content = db.Column(db.Text, nullable=False)                           # Markdown 内容
    difficulty = db.Column(db.Integer, default=3)                          # 难度 1-5
    mastery_level = db.Column(db.Integer, default=0)                       # 掌握程度 0-5
    is_mistake = db.Column(db.Boolean, default=False)                      # 易错知识点标记
    file_path = db.Column(db.String(256), nullable=True)                   # 关联文件路径
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    tags = db.relationship('Tag', secondary='note_tags', backref='notes', lazy='dynamic')
    review_plans = db.relationship('ReviewPlan', backref='note', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Note {self.title}>'
