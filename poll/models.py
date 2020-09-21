from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

db = SQLAlchemy()


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(GUID(), unique=True, default=uuid.uuid4)
    question = db.Column(db.String(1000), nullable=False)
    access_key = db.Column(db.String(255), unique=False, nullable=False)
    max_selection_limit = db.Column(db.Integer, default=1)
    answers = db.relationship('Answer', backref='poll',
                              lazy=True, cascade="all, delete")
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return '<Question %r>' % self.question

    def to_json(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'question': self.question,
            'access_key': self.access_key,
            'max_selection_limit': self.max_selection_limit,
        }
    
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), unique=False, nullable=False)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'),
                        nullable=False)
    votes = db.relationship('Vote', backref='answer',
                            lazy=True, cascade="all, delete")

    def __repr__(self):
        return '<Answer %r>' % self.text

    def to_json(self):
        return {
            'id': self.id,
            'text': self.text,
            'poll_id': self.poll_id,
        }


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter = db.Column(db.String(255), unique=False, nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'),
                          nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return '<Voter %r>' % self.voter
    
    def to_json(self):
        return {
            'id': self.id,
            'voter': self.voter,
            'answer_id': self.answer_id,
        }