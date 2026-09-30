from flask_sqlalchemy import SQLAlchemy

# Initialize the extension globally, but don't bind it to an app yet
db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = 'books'
    
    isbn = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    borrowed_by = db.Column(db.String(20), db.ForeignKey('members.member_id'), default=None, nullable=True)

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "is_available": self.is_available,
            "borrowed_by": self.borrowed_by
        }


class Member(db.Model):
    __tablename__ = 'members'
    
    BORROW_LIMIT = 3
    
    member_id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    borrowed_books = db.relationship('Book', backref='borrower', lazy=True)

    def to_dict(self):
        return {
            "name": self.name,
            "member_id": self.member_id,
            "borrowed_books": [b.title for b in self.borrowed_books]
        }
