from datetime import datetime
from apps import db

class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(100), nullable=False)
    flag_url = db.Column(db.String(200), nullable=False)   # from Flagpedia API
    correct_answer = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, default=1)   # Level system (set of 10)

    def __repr__(self):
        return f"<Question {self.country_name}>"


class UserProgress(db.Model):
    __tablename__ = "user_progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("Users", backref="progress", lazy=True)
    question = db.relationship("Question", backref="attempts", lazy=True)

    def __repr__(self):
        return f"<UserProgress User={self.user_id} Question={self.question_id}>"
