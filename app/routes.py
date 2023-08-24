from app import db
from flask import Blueprint, request, jsonify, make_response
from app.models.flashcard import Flashcard

flashcards_bp = Blueprint("flashcards", __name__, url_prefix="/flashcards")

@flashcards_bp.route("", methods=["POST"])
def create_one_flashcard():
    request_body = request.get_json()
    new_flashcard = Flashcard(term=request_body["term"], explanation=request_body["explanation"])

    db.session.add(new_flashcard)
    db.session.commit()

    return make_response(f"Flashcard {new_flashcard.term} successfully created", 201)
