from flask import render_template, request, jsonify, current_app
from app.models import db, Book, Member

# We use the current_app context proxy to bind mappings cleanly
@current_app.route("/")
def index():
    return render_template("index.html")

@current_app.route("/api/data", methods=["GET"])
def get_data():
    books = Book.query.all()
    members = Member.query.all()
    return jsonify({
        "books": [b.to_dict() for b in books],
        "members": [m.to_dict() for m in members]
    })

@current_app.route("/api/add_book", methods=["POST"])
def add_book_api():
    data = request.get_json()
    isbn = data.get("isbn")
    if Book.query.get(isbn):
        return jsonify({"success": False, "message": f"A book with ISBN {isbn} already exists."})
    
    new_book = Book(title=data.get("title"), author=data.get("author"), isbn=isbn)
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"success": True, "message": f"Book '{new_book.title}' added successfully."})

@current_app.route("/api/add_member", methods=["POST"])
def add_member_api():
    data = request.get_json()
    member_id = data.get("member_id")
    if Member.query.get(member_id):
        return jsonify({"success": False, "message": f"A member with ID {member_id} already exists."})
        
    new_member = Member(name=data.get("name"), member_id=member_id)
    db.session.add(new_member)
    db.session.commit()
    return jsonify({"success": True, "message": f"Member '{new_member.name}' registered successfully."})

@current_app.route("/api/delete_book", methods=["POST"])
def delete_book_api():
    data = request.get_json()
    book = Book.query.get(data.get("isbn"))
    if not book:
        return jsonify({"success": False, "message": "Book ISBN not found in inventory."})
    if not book.is_available:
        return jsonify({"success": False, "message": f"Cannot delete '{book.title}' while it is borrowed."})
        
    db.session.delete(book)
    db.session.commit()
    return jsonify({"success": True, "message": f"Book '{book.title}' deleted successfully."})

@current_app.route("/api/delete_member", methods=["POST"])
def delete_member_api():
    data = request.get_json()
    member = Member.query.get(data.get("member_id"))
    if not member:
        return jsonify({"success": False, "message": "Member ID not registered."})
    if len(member.borrowed_books) > 0:
        return jsonify({"success": False, "message": f"Cannot delete {member.name} while they have borrowed books."})
        
    db.session.delete(member)
    db.session.commit()
    return jsonify({"success": True, "message": f"Member '{member.name}' deleted successfully."})

@current_app.route("/api/borrow", methods=["POST"])
def borrow_api():
    data = request.get_json()
    member = Member.query.get(data.get("member_id"))
    book = Book.query.get(data.get("isbn"))
    
    if not member: return jsonify({"success": False, "message": "Member ID not registered."})
    if not book: return jsonify({"success": False, "message": "Book ISBN not found in inventory."})
    
    if len(member.borrowed_books) >= Member.BORROW_LIMIT:
        return jsonify({"success": False, "message": f"Rejected: {member.name} has hit the borrow max limit ({Member.BORROW_LIMIT} books)."})
    if not book.is_available:
        return jsonify({"success": False, "message": f"Sorry, '{book.title}' is already borrowed."})
        
    book.is_available = False
    member.borrowed_books.append(book)
    db.session.commit()
    return jsonify({"success": True, "message": f"Successfully borrowed '{book.title}'."})

@current_app.route("/api/return", methods=["POST"])
def return_api():
    data = request.get_json()
    member = Member.query.get(data.get("member_id"))
    book = Book.query.get(data.get("isbn"))
    
    if not member: return jsonify({"success": False, "message": "Member ID not registered."})
    if not book: return jsonify({"success": False, "message": "Book ISBN not found in inventory."})
    
    if book not in member.borrowed_books:
        return jsonify({"success": False, "message": f"Rejected: {member.name} does not have '{book.title}' checked out."})
        
    book.is_available = True
    member.borrowed_books.remove(book)
    db.session.commit()
    return jsonify({"success": True, "message": f"Successfully returned '{book.title}'."})
