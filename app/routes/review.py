"""复习计划路由"""

from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.review_plan import ReviewPlan
from app.models.note import Note

review_bp = Blueprint('review', __name__, template_folder='../templates')


@review_bp.route('/')
@login_required
def review_today():
    """今日待复习列表"""
    today = date.today()

    pending_reviews = ReviewPlan.query.filter(
        ReviewPlan.user_id == current_user.id,
        ReviewPlan.status == 'pending',
        db.func.date(ReviewPlan.review_date) <= today
    ).order_by(ReviewPlan.review_date.asc()).all()

    # 按知识点分组
    review_groups = {}
    for r in pending_reviews:
        if r.note_id not in review_groups:
            review_groups[r.note_id] = {
                'note': r.note,
                'plans': []
            }
        review_groups[r.note_id]['plans'].append(r)

    return render_template('review_today.html',
                           review_groups=review_groups)


@review_bp.route('/complete/<int:plan_id>', methods=['POST'])
@login_required
def complete_review(plan_id):
    """完成一次复习"""
    plan = ReviewPlan.query.get_or_404(plan_id)
    if plan.user_id != current_user.id:
        flash('无权限', 'danger')
        return redirect(url_for('review.review_today'))

    plan.status = 'completed'
    plan.completed_at = datetime.utcnow()
    db.session.commit()

    flash('复习完成！', 'success')
    return redirect(url_for('review.review_today'))


@review_bp.route('/history')
@login_required
def review_history():
    """复习历史"""
    page = request.args.get('page', 1, type=int)

    pagination = ReviewPlan.query.filter(
        ReviewPlan.user_id == current_user.id,
        ReviewPlan.status == 'completed'
    ).order_by(ReviewPlan.completed_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('review_history.html', pagination=pagination)
