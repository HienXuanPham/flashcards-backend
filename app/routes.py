from sqlalchemy import func
from app import db
from flask import Blueprint, request, jsonify, make_response, abort
from app.models.flashcard import Flashcard

flashcards_bp = Blueprint("flashcards", __name__, url_prefix="/flashcards")

# Helper function
def validate_flashcard(cls, flashcard_id):
    try:
        flashcard_id = int(flashcard_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {flashcard_id} invalid"}, 400))

    flashcard = db.session.get(Flashcard, flashcard_id)

    if not flashcard:
        abort(make_response({"message": f"{cls.__name__} #{flashcard_id} not found"}, 404))

    return flashcard

def validate_request(cls, request_data):
    try:
        new_object = cls.create_new_object_from_request_data(request_data)
    except KeyError as e:
        abort(make_response({"message": f"Request body must include {e}"}), 400)

    return new_object

# Routes
@flashcards_bp.route("", methods=["POST"])
def create_one_flashcard():
    request_body = request.get_json()
    new_flashcard = validate_request(Flashcard, request_body)

    db.session.add(new_flashcard)
    db.session.commit()

    return make_response(f"Flashcard {new_flashcard.term} successfully created", 201)

@flashcards_bp.route("", methods=["GET"])
def read_all_flashcards_or_read_by_term():
    term_query = request.args.get("term")
    if term_query:
        flashcards_query = Flashcard.query.filter(func.lower(Flashcard.term) == term_query.lower())
    else:
        flashcards_query = Flashcard.query.all()

    flashcards_response = []
    for flashcard in flashcards_query:
        flashcards_response.append(flashcard.convert_to_dictionary())

    return make_response(jsonify(flashcards_response), 200)

@flashcards_bp.route("/<flashcard_id>", methods=["PUT"])
def update_flashcard(flashcard_id):
    flashcard = validate_flashcard(Flashcard, flashcard_id)

    request_body = request.get_json()
    request_body_validated = validate_request(Flashcard, request_body)

    if request_body_validated:
        flashcard.term = request_body_validated.term
        flashcard.explanation = request_body_validated.explanation

        db.session.commit()

    return make_response(jsonify(flashcard.convert_to_dictionary()), 200)

@flashcards_bp.route("/<flashcard_id>", methods=["DELETE"])
def delete_flashcard(flashcard_id):
    flashcard = validate_flashcard(Flashcard, flashcard_id)

    db.session.delete(flashcard)
    db.session.commit()

    return make_response(f"Flashcard #{flashcard_id} successfully deleted.")
