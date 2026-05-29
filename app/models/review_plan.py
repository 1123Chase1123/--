"""复习计划模型 —— 基于艾宾浩斯遗忘曲线"""

from datetime import datetime
from app import db


class ReviewPlan(db.Model):
    __tablename__ = 'review_plan'

    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    review_date = db.Column(db.DateTime, nullable=False, index=True)       # 计划复习日期
    review_count = db.Column(db.Integer, default=0)                        # 已复习次数
    status = db.Column(db.String(20), default='pending')                   # pending / completed / skipped
    completed_at = db.Column(db.DateTime, nullable=True)                   # 实际完成时间
    next_review_date = db.Column(db.DateTime, nullable=True)               # 下次复习日期
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ReviewPlan note={self.note_id} date={self.review_date}>'
