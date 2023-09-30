from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)

def test_filter_and_search():
    response = client.get("/books/")
    assert response.status_code == 200

test_filter_and_search()