import pytest
from app import create_app
from app.models import db, Book, Member

@pytest.fixture
def app():
    """Sets up a temporary Flask application instance for testing."""
    app = create_app()
    # Switch out the real database file for a temporary in-memory database
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    # Spin up clean tables inside the test environment
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Provides a virtual test client to make API requests."""
    return app.test_client()

# ==========================================
# 1. TEST DATABASE CORE MODELS
# ==========================================
def test_create_book_and_member(app):
    """Verifies that items can be inserted into the database accurately."""
    with app.app_context():
        book = Book(title="Test-Driven Development", author="Kent Beck", isbn="999")
        member = Member(name="Tester John", member_id="T01")
        
        db.session.add(book)
        db.session.add(member)
        db.session.commit()

        assert Book.query.get("999").title == "Test-Driven Development"
        assert Member.query.get("T01").name == "Tester John"

# ==========================================
# 2. TEST API ROUTING ENDPOINTS
# ==========================================
def test_get_data_api(client):
    """Ensures the data API endpoint returns a valid structural layout."""
    response = client.get("/api/data")
    assert response.status_code == 200
    
    data = response.get_json()
    assert "books" in data
    assert "members" in data

def test_add_book_api(client):
    """Tests if adding a book via POST request inserts records correctly."""
    payload = {"title": "Clean Code", "author": "Robert Martin", "isbn": "777"}
    response = client.post("/api/add_book", json=payload)
    
    assert response.status_code == 200
    assert response.get_json()["success"] is True

# ==========================================
# 3. TEST CIRCULATION BUSINESS LOGIC
# ==========================================
def test_borrow_limit_enforcement(app, client):
    """Verifies a member cannot borrow more than the max limit (3 books)."""
    with app.app_context():
        # 1. Register a member
        member = Member(name="Avid Reader", member_id="M99")
        db.session.add(member)
        
        # 2. Add 4 different books to the catalog
        for i in range(1, 5):
            book = Book(title=f"Volume {i}", author="Author", isbn=f"20{i}")
            db.session.add(book)
        db.session.commit()

    # Try to borrow all 4 books sequentially via the API
    for i in range(1, 4):
        res = client.post("/api/borrow", json={"member_id": "M99", "isbn": f"20{i}"})
        assert res.get_json()["success"] is True

    # The 4th book attempt must be rejected by the validation rules
    failed_res = client.post("/api/borrow", json={"member_id": "M99", "isbn": "204"})
    assert failed_res.get_json()["success"] is False
    assert "hit the borrow max limit" in failed_res.get_json()["message"]
