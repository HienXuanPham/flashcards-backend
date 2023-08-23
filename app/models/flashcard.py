from app import db

class Flashcard(db.Model):
    flashcard_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    term = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text, nullable=False)
    