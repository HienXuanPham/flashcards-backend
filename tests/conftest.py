import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.flashcard import Flashcard

@pytest.fixture
def app():
  app = create_app({"TESTING": True})

  @request_finished.connect_via(app)
  def expire_session(sender, response, **extra):
    db.session.remove()

  with app.app_context():
    db.create_all()
    yield app

  with app.app_context():
    db.drop_all()


@pytest.fixture
def client(app):
  return app.test_client()

@pytest.fixture
def three_saved_flashcards(app):
  fixture_flashcard = Flashcard(term="fixture", explanation="In testing, a fixture provides a defined, reliable and consistent context for the tests")
  fixture_dependency_flashcard = Flashcard(term="dependency", explanation="a fixture listed as one of the parameters in a test function")
  dependency_injection_flashcard = Flashcard(term="dependency injection", explanation="A way for code to explicitly declare and receive the resources it needs to run successfully")

  db.session.add_all([fixture_flashcard, fixture_dependency_flashcard, dependency_injection_flashcard])
  db.session.commit()
