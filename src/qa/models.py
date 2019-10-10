from src.base.base_models import BaseDateTimeModel
from src.extensions import db


class Chapter(db.Model):
    __tablename__ = 'chapters'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)  # noqa: A003
    name = db.Column(db.Text(), nullable=False)
    order_number = db.Column(db.Integer, nullable=False)
    questions = db.relationship('Question', back_populates='chapter')


class Question(BaseDateTimeModel):
    __tablename__ = 'questions'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)  # noqa: A003
    text = db.Column(db.Text(), nullable=False)
    order_number = db.Column(db.Integer, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    answers = db.relationship(
        'Answer', backref='questions', lazy='dynamic',
    )
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'))
    chapter = db.relationship(
        'Chapter', back_populates='questions')

    def __repr__(self):
        return self.text


class Answer(BaseDateTimeModel):
    __tablename__ = 'answers'
    __table_args__ = {'extend_existing': True}

    def __init__(self, text, question_id):
        self.text = text
        self.question_id = question_id

    id = db.Column(db.Integer, primary_key=True)  # noqa: A003
    text = db.Column(db.Text(), nullable=False)
    is_approve = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
