from app import db

class Flashcard(db.Model):
    flashcard_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    term = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text, nullable=False)
    

    def convert_to_dict(self):
        flashcard_dict = {
            "flashcard_id": self.flashcard_id,
            "term": self.term,
            "explanation": self.explanation
        }

        return flashcard_dict
