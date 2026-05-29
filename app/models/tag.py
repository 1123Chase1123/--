"""标签模型 + 知识点-标签关联表"""

from app import db


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(50), unique=True, nullable=False, index=True)

    def __repr__(self):
        return f'<Tag {self.tag_name}>'


class NoteTag(db.Model):
    __tablename__ = 'note_tags'

    note_id = db.Column(db.Integer, db.ForeignKey('notes.id', ondelete='CASCADE'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)

    def __repr__(self):
        return f'<NoteTag note={self.note_id} tag={self.tag_id}>'
