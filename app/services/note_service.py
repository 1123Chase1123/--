"""知识点业务逻辑"""

from datetime import datetime
from app import db
from app.models.note import Note
from app.models.tag import Tag, NoteTag
from app.models.review_plan import ReviewPlan
from app.utils.subject_manager import load_subjects


class NoteService:
    """知识点 CRUD + 标签管理 + 复习计划生成"""

    @staticmethod
    def get_subjects():
        """从 subjects.json 动态读取科目列表"""
        return load_subjects()

    # ---- 知识点 CRUD ----

    @staticmethod
    def create_note(user_id, title, content, subject, chapter=None,
                    difficulty=3, tags=None, file_path=None) -> tuple[bool, str, Note]:
        """创建知识点"""
        if not title or not title.strip():
            return False, '标题不能为空', None
        if not content or not content.strip():
            return False, '内容不能为空', None
        if not subject or not subject.strip():
            return False, '请选择或输入科目', None

        note = Note(
            user_id=user_id,
            subject=subject,
            chapter=chapter,
            title=title.strip(),
            content=content,
            difficulty=difficulty,
            file_path=file_path,
        )
        db.session.add(note)
        db.session.flush()  # 获取 note.id

        # 关联标签
        if tags:
            NoteService._set_tags(note, tags)

        db.session.commit()

        # 自动生成复习计划
        NoteService._generate_review_plan(note)

        return True, '知识点创建成功', note

    @staticmethod
    def update_note(note, title, content, subject, chapter=None,
                    difficulty=3, mastery_level=0, is_mistake=False, tags=None) -> tuple[bool, str]:
        """更新知识点"""
        note.title = title.strip()
        note.content = content
        note.subject = subject
        note.chapter = chapter
        note.difficulty = difficulty
        note.mastery_level = mastery_level
        note.is_mistake = is_mistake
        note.updated_at = datetime.utcnow()

        if tags is not None:
            NoteService._set_tags(note, tags)

        db.session.commit()
        return True, '知识点更新成功'

    @staticmethod
    def delete_note(note) -> tuple[bool, str]:
        """删除知识点"""
        db.session.delete(note)
        db.session.commit()
        return True, '知识点已删除'

    @staticmethod
    def get_note_by_id(note_id):
        """获取单个知识点"""
        return Note.query.get(note_id)

    @staticmethod
    def get_user_notes(user_id, subject=None, tag=None, search=None,
                       page=1, per_page=20):
        """获取用户的知识点列表，支持筛选和分页"""
        query = Note.query.filter_by(user_id=user_id)

        if subject:
            query = query.filter_by(subject=subject)
        if tag:
            query = query.join(Note.tags).filter(Tag.tag_name == tag)
        if search:
            like_pattern = f'%{search}%'
            query = query.filter(
                db.or_(Note.title.ilike(like_pattern),
                       Note.content.ilike(like_pattern))
            )

        query = query.order_by(Note.updated_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination

    # ---- 标签管理 ----

    @staticmethod
    def _set_tags(note, tag_names: list[str]):
        """为知识点设置标签（先清空再重建）"""
        # 清空旧标签关联
        NoteTag.query.filter_by(note_id=note.id).delete()

        for name in tag_names:
            name = name.strip()
            if not name:
                continue
            tag = Tag.query.filter_by(tag_name=name).first()
            if not tag:
                tag = Tag(tag_name=name)
                db.session.add(tag)
                db.session.flush()
            note_tag = NoteTag(note_id=note.id, tag_id=tag.id)
            db.session.add(note_tag)

    @staticmethod
    def get_all_tags(user_id=None):
        """获取所有标签（可过滤用户已使用的）"""
        if user_id:
            return Tag.query.join(NoteTag).join(Note).filter(
                Note.user_id == user_id
            ).distinct().all()
        return Tag.query.all()

    # ---- 复习计划 ----

    @staticmethod
    def _generate_review_plan(note):
        """艾宾浩斯遗忘曲线复习间隔（天）"""
        intervals = [1, 3, 7, 15, 30]

        for i, days in enumerate(intervals):
            from datetime import timedelta
            review_date = datetime.utcnow() + timedelta(days=days)

            plan = ReviewPlan(
                note_id=note.id,
                user_id=note.user_id,
                review_date=review_date,
                review_count=i + 1,
                status='pending',
                next_review_date=review_date + timedelta(days=intervals[i + 1]) if i + 1 < len(intervals) else None,
            )
            db.session.add(plan)

        db.session.commit()
