from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ==========================================
# SYSTEM CORE CLASSES
# ==========================================
class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True

    # Converts class object attributes to a standard python dictionary for JSON conversion
    def to_dict(self):
        return {"title": self.title, "author": self.author, "isbn": self.isbn, "is_available": self.is_available}

    def borrow_book(self):
        if not self.is_available:
            return False, f"Sorry, '{self.title}' is already borrowed."
        self.is_available = False
        return True, f"Successfully borrowed '{self.title}'."

    def return_book(self):
        if self.is_available:
            return False, f"'{self.title}' was not borrowed."
        self.is_available = True
        return True, f"Successfully returned '{self.title}'."


class Member:
    BORROW_LIMIT = 3
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []

    def to_dict(self):
        return {
            "name": self.name,
            "member_id": self.member_id,
            "borrowed_books": [b.title for b in self.borrowed_books]
        }

    def borrow_book(self, book):
        if len(self.borrowed_books) >= self.BORROW_LIMIT:
            return False, f"Rejected: {self.name} has hit the borrow max limit ({self.BORROW_LIMIT} books)."
        success, message = book.borrow_book()
        if success:
            self.borrowed_books.append(book)
        return success, message

    def return_book(self, book):
        if book in self.borrowed_books:
            success, message = book.return_book()
            if success:
                self.borrowed_books.remove(book)
            return success, message
        return False, f"Rejected: {self.name} does not have '{book.title}' checked out."


class Library:
    def __init__(self):
        self.books = []
        self.members = []

    def add_book(self, title, author, isbn):
        if self.find_book(isbn):
            return False, f"A book with ISBN {isbn} already exists."
        self.books.append(Book(title, author, isbn))
        return True, f"Book '{title}' added successfully."

    def add_member(self, name, member_id):
        if self.find_member(member_id):
            return False, f"A member with ID {member_id} already exists."
        self.members.append(Member(name, member_id))
        return True, f"Member '{name}' registered successfully."

    def find_book(self, isbn):
        return next((b for b in self.books if b.isbn == isbn), None)

    def find_member(self, member_id):
        return next((m for m in self.members if m.member_id == member_id), None)

    def delete_book(self, isbn):
        book = self.find_book(isbn)
        if not book:
            return False, "Book ISBN not found in inventory."
        if not book.is_available:
            return False, f"Cannot delete '{book.title}' while it is borrowed."
        self.books.remove(book)
        return True, f"Book '{book.title}' deleted successfully."

    def delete_member(self, member_id):
        member = self.find_member(member_id)
        if not member:
            return False, "Member ID not registered."
        if member.borrowed_books:
            return False, f"Cannot delete {member.name} while they have borrowed books."
        self.members.remove(member)
        return True, f"Member '{member.name}' deleted successfully."

    def process_borrow(self, member_id, isbn):
        member = self.find_member(member_id)
        book = self.find_book(isbn)
        if not member: return False, "Member ID not registered."
        if not book: return False, "Book ISBN not found in inventory."
        return member.borrow_book(book)

    def process_return(self, member_id, isbn):
        member = self.find_member(member_id)
        book = self.find_book(isbn)
        if not member: return False, "Member ID not registered."
        if not book: return False, "Book ISBN not found in inventory."
        return member.return_book(book)

# Initialize application database framework instance
library = Library()
library.add_book("Python Basics", "Lawrence", "101")
library.add_book("Data Structures", "Alice", "102")
library.add_book("48 Law's of Power", "Robert Greene", "103")
library.add_book("The Trials Of Brother Jehro", "Wole Soyinka", "104")
library.add_book("The Song of Ice and Fire", "George R.R. Martin", "105")
library.add_member("Lawrence Ogbaji", "M01")
library.add_member("Jane Smith", "M02")


# ==========================================
# BACKEND API ROUTING ENDPOINTS
# ==========================================
@app.route("/")
def index():
    return render_template("index.html") # Loads the raw dashboard frame empty

@app.route("/api/data", methods=["GET"])
def get_data():
    # Package data cleanly into standard dictionaries to send over the network
    return jsonify({
        "books": [b.to_dict() for b in library.books],
        "members": [m.to_dict() for m in library.members]
    })

@app.route("/api/add_book", methods=["POST"])
def add_book_api():
    data = request.get_json()
    success, message = library.add_book(data.get("title"), data.get("author"), data.get("isbn"))
    return jsonify({"success": success, "message": message})

@app.route("/api/add_member", methods=["POST"])
def add_member_api():
    data = request.get_json()
    success, message = library.add_member(data.get("name"), data.get("member_id"))
    return jsonify({"success": success, "message": message})

@app.route("/api/delete_book", methods=["POST"])
def delete_book_api():
    data = request.get_json()
    success, message = library.delete_book(data.get("isbn"))
    return jsonify({"success": success, "message": message})

@app.route("/api/delete_member", methods=["POST"])
def delete_member_api():
    data = request.get_json()
    success, message = library.delete_member(data.get("member_id"))
    return jsonify({"success": success, "message": message})

@app.route("/api/borrow", methods=["POST"])
def borrow_api():
    data = request.get_json()
    success, message = library.process_borrow(data.get("member_id"), data.get("isbn"))
    return jsonify({"success": success, "message": message})

@app.route("/api/return", methods=["POST"])
def return_api():
    data = request.get_json()
    success, message = library.process_return(data.get("member_id"), data.get("isbn"))
    return jsonify({"success": success, "message": message})

if __name__ == "__main__":
    app.run(debug=True)
