def test_create_one_flashcard(client):
  test_data = {
    "term": "안녕하세요",
    "explanation": "hello"
  }

  response = client.post("/flashcards", json=test_data)
  response_body = response.get_data(as_text=True)

  assert response.status_code == 201
  assert response_body == "Flashcard 안녕하세요 successfully created"

def test_get_flashcards_no_saved_flashcards(client):
  response = client.get("/flashcards")
  response_body = response.get_json()

  assert response.status_code == 200
  assert response_body == []

def test_get_all_flashcards(client, three_saved_flashcards):
  response = client.get("/flashcards")
  response_body = response.get_json()

  assert response.status_code == 200
  assert len(response_body) == 3
  assert response_body == [{'explanation': 'In testing, a fixture provides a defined, reliable and consistent context for the tests', 'flashcard_id': 1, 'term': 'fixture'}, {'explanation': 'a fixture listed as one of the parameters in a test function', 'flashcard_id': 2, 'term': 'dependency'}, {'explanation': 'A way for code to explicitly declare and receive the resources it needs to run successfully', 'flashcard_id': 3, 'term': 'dependency injection'}]

def test_get_flashcard_by_term(client, three_saved_flashcards):
  response = client.get("/flashcards?term=fixture")
  response_body = response.get_json()

  assert response.status_code == 200
  assert len(response_body) == 1
  assert response_body == [{'explanation': 'In testing, a fixture provides a defined, reliable and consistent context for the tests', 'flashcard_id': 1, 'term': 'fixture'}]

def test_get_flashcard_by_term_no_saved_term(client, three_saved_flashcards):
  response = client.get("/flashcards?term=hello world")
  response_body = response.get_json()

  assert response.status_code == 200
  assert len(response_body) == 0
  assert response_body == []

def test_update_flashcard(client, three_saved_flashcards):
  response = client.put("/flashcards/1", json={
    "term": "fixture",
    "explanation": "Shared code used to perform setup and cleanup for test"
  })
  response_body = response.get_json()
  print(response_body)

  assert response.status_code == 200
  assert response_body ==  {'explanation': 'Shared code used to perform setup and cleanup for test', 'flashcard_id': 1, 'term': 'fixture'}

def test_delete_one_flashcard(client, three_saved_flashcards):
  response = client.delete("/flashcards/1")
  response_body = response.get_data(as_text=True)

  assert response.status_code == 200
  assert response_body == "Flashcard #1 successfully deleted."
