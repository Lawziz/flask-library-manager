import os
from flask import Flask
from app.models import db, Book, Member

def create_app():
    app = Flask(__name__)


    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../library.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    db.init_app(app)

    # Import and register the blueprint here
    from app.routes import main
    app.register_blueprint(main)



    with app.app_context():
        db.create_all()
        seed_database()

    return app



def seed_database():
    if Book.query.first() is None and Member.query.first() is None:
        default_books = [
            Book(title="Python Basics", author="Lawrence", isbn="101"),
            Book(title="Data Structures", author="Alice", isbn="102"),
            Book(title="48 Laws of Power", author="Robert Greene", isbn="103"),
            Book(title="The Trials Of Brother Jero", author="Wole Soyinka", isbn="104"),
            Book(title="The Song of Ice and Fire", author="George R.R. Martin", isbn="105")
        ]
        default_members = [
            Member(name="Lawrence Ogbaji", member_id="M01"),
            Member(name="Jane Smith", member_id="M02")
        ]
        db.session.add_all(default_books + default_members)
        db.session.commit()
