from sqlalchemy import func
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

@flashcards_bp.route("", methods=["GET"])
def read_all_flashcards():
    term_query = request.args.get("term")
    if term_query:
        flashcards_query = Flashcard.query.filter(func.lower(Flashcard.term) == term_query.lower())
    else:
        flashcards_query = Flashcard.query.all()

    flashcards_response = []
    for flashcard in flashcards_query:
        flashcards_response.append(flashcard.convert_to_dict())

    return make_response(jsonify(flashcards_response), 200)