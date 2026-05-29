"""知识点管理路由"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.services.note_service import NoteService
from app.utils.file_handler import save_upload
from app.utils.subject_manager import add_subject

notes_bp = Blueprint('notes', __name__, template_folder='../templates')


@notes_bp.route('/dashboard')
@login_required
def dashboard():
    """主页 Dashboard"""
    from datetime import date
    today = date.today()
    from app.models.review_plan import ReviewPlan

    total_notes = NoteService.get_user_notes(current_user.id).total
    pending_reviews = ReviewPlan.query.filter(
        ReviewPlan.user_id == current_user.id,
        ReviewPlan.status == 'pending',
        db.func.date(ReviewPlan.review_date) <= today
    ).count()

    recent_notes = NoteService.get_user_notes(
        current_user.id, page=1, per_page=5
    ).items

    return render_template('dashboard.html',
                           total_notes=total_notes,
                           pending_reviews=pending_reviews,
                           recent_notes=recent_notes)


@notes_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_note():
    """创建知识点"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '')
        subject = request.form.get('subject', '')
        chapter = request.form.get('chapter', '').strip() or None
        difficulty = int(request.form.get('difficulty', 3))
        tag_names = request.form.getlist('tags') or []

        # 处理标签（逗号分隔）
        tags_flat = []
        for t in tag_names:
            tags_flat.extend([x.strip() for x in t.split(',') if x.strip()])

        # 处理文件上传
        file_path = None
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename:
                success, result = save_upload(file)
                if success:
                    file_path = result

        # 保存新建的科目
        add_subject(subject)

        success, message, note = NoteService.create_note(
            user_id=current_user.id,
            title=title,
            content=content,
            subject=subject,
            chapter=chapter,
            difficulty=difficulty,
            tags=tags_flat,
            file_path=file_path,
        )
        if success:
            flash(message, 'success')
            return redirect(url_for('notes.note_detail', note_id=note.id))
        flash(message, 'danger')

    subjects = NoteService.get_subjects()
    return render_template('create_note.html', subjects=subjects)


@notes_bp.route('/<int:note_id>')
@login_required
def note_detail(note_id):
    """知识点详情"""
    note = NoteService.get_note_by_id(note_id)
    if not note or note.user_id != current_user.id:
        flash('知识点不存在', 'danger')
        return redirect(url_for('notes.dashboard'))
    return render_template('note_detail.html', note=note)


@notes_bp.route('/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    """编辑知识点"""
    note = NoteService.get_note_by_id(note_id)
    if not note or note.user_id != current_user.id:
        flash('知识点不存在', 'danger')
        return redirect(url_for('notes.dashboard'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '')
        subject = request.form.get('subject', '')
        chapter = request.form.get('chapter', '').strip() or None
        difficulty = int(request.form.get('difficulty', 3))
        mastery_level = int(request.form.get('mastery_level', 0))
        is_mistake = request.form.get('is_mistake') == 'on'
        tag_names = request.form.getlist('tags') or []

        tags_flat = []
        for t in tag_names:
            tags_flat.extend([x.strip() for x in t.split(',') if x.strip()])

        # 保存新建的科目
        add_subject(subject)

        success, message = NoteService.update_note(
            note, title, content, subject, chapter,
            difficulty, mastery_level, is_mistake, tags_flat
        )
        if success:
            flash(message, 'success')
            return redirect(url_for('notes.note_detail', note_id=note.id))
        flash(message, 'danger')

    subjects = NoteService.get_subjects()
    return render_template('edit_note.html', note=note, subjects=subjects)


@notes_bp.route('/<int:note_id>/delete', methods=['POST'])
@login_required
def delete_note(note_id):
    """删除知识点"""
    note = NoteService.get_note_by_id(note_id)
    if not note or note.user_id != current_user.id:
        flash('知识点不存在', 'danger')
        return redirect(url_for('notes.dashboard'))

    NoteService.delete_note(note)
    flash('知识点已删除', 'success')
    return redirect(url_for('notes.dashboard'))


@notes_bp.route('/history')
@login_required
def history():
    """历史记录页"""
    subject = request.args.get('subject', '')
    tag = request.args.get('tag', '')
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)

    pagination = NoteService.get_user_notes(
        current_user.id, subject=subject, tag=tag,
        search=search, page=page
    )
    subjects = NoteService.get_subjects()
    tags = NoteService.get_all_tags(user_id=current_user.id)

    return render_template('history.html',
                           pagination=pagination,
                           subjects=subjects,
                           tags=tags,
                           current_subject=subject,
                           current_tag=tag,
                           current_search=search)
