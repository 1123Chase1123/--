"""数据统计路由"""

from datetime import datetime, date, timedelta
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.note import Note
from app.models.review_plan import ReviewPlan

statistics_bp = Blueprint('statistics', __name__, template_folder='../templates')


@statistics_bp.route('/')
@login_required
def statistics():
    """统计分析页面"""
    return render_template('statistics.html')


@statistics_bp.route('/api/summary')
@login_required
def api_summary():
    """统计摘要数据 API"""
    user_id = current_user.id

    # 总知识点数
    total_notes = Note.query.filter_by(user_id=user_id).count()

    # 各科目数量
    subjects_data = db.session.query(
        Note.subject, db.func.count(Note.id)
    ).filter(Note.user_id == user_id).group_by(Note.subject).all()

    # 总复习次数
    total_reviews = ReviewPlan.query.filter(
        ReviewPlan.user_id == user_id,
        ReviewPlan.status == 'completed'
    ).count()

    # 待复习数
    pending = ReviewPlan.query.filter(
        ReviewPlan.user_id == user_id,
        ReviewPlan.status == 'pending',
        db.func.date(ReviewPlan.review_date) <= date.today()
    ).count()

    # 掌握程度分布
    mastery_data = db.session.query(
        Note.mastery_level, db.func.count(Note.id)
    ).filter(Note.user_id == user_id).group_by(Note.mastery_level).all()

    # 近7天复习记录
    review_trend = []
    for i in range(6, -1, -1):
        day = date.today() - timedelta(days=i)
        count = ReviewPlan.query.filter(
            ReviewPlan.user_id == user_id,
            ReviewPlan.status == 'completed',
            db.func.date(ReviewPlan.completed_at) == day
        ).count()
        review_trend.append({
            'date': day.strftime('%m-%d'),
            'count': count
        })

    return jsonify({
        'total_notes': total_notes,
        'subjects': {s: c for s, c in subjects_data},
        'total_reviews': total_reviews,
        'pending_reviews': pending,
        'mastery': {str(m): c for m, c in mastery_data},
        'review_trend': review_trend,
    })
