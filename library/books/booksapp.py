from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    editor = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    avaiablecopies = db.Column(db.Integer, nullable=False)

    def json(self):
        return {'id': self.id, 'title': self.title, 'author': self.author, 'editor': self.editor, 'year': self.year, 'avaiablecopies': self.avaiablecopies}

db.create_all()

#create a test route
@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route'}), 200)


@app.route('/books', methods=['POST'])
def newbook():
  try:
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'], editor=data['editor'], year=data['year'], avaiablecopies=data['avaiablecopies'])
    db.session.add(new_book)
    db.session.commit()
    return make_response(jsonify({'message': 'book added'}), 201)
  except Exception as e:
    print(str(e))
    return make_response(jsonify({'message': 'error adding book'}), 500)


@app.route('/books', methods=['GET'])
def get_books():
  try:
    books = Book.query.all()
    return make_response(jsonify([book.json() for book in books]), 200)
  except Exception as e:
    print(str(e))
    return make_response(jsonify({'message': 'error getting books'}), 500)


@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
  try:
    book = Book.query.filter_by(id=id).first()
    if book:
      return make_response(jsonify({'user': book.json()}), 200)
    return make_response(jsonify({'message': 'book not found'}), 404)
  except Exception as e:
    print(str(e))
    return make_response(jsonify({'message': 'error getting the book'}), 500)


@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
  try:
    book = Book.query.filter_by(id=id).first()
    if book:
      data = request.get_json()
      book.title = data['title']
      book.author = data['author']
      book.editor = data['editor']
      book.year = data['year']
      book.avaiablecopies = data['avaiablecopies']
      db.session.commit()
      return make_response(jsonify({'message': 'book updated'}), 200)
    return make_response(jsonify({'message': 'book not found'}), 404)
  except Exception as e:
    print(str(e))
    return make_response(jsonify({'message': 'error updating book'}), 500)

# delete a user
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_user(id):
  try:
    book = Book.query.filter_by(id=id).first()
    if book:
      db.session.delete(book)
      db.session.commit()
      return make_response(jsonify({'message': 'book deleted'}), 200)
    return make_response(jsonify({'message': 'book not found'}), 404)
  except Exception as e:
    print(str(e))
    return make_response(jsonify({'message': 'error deleting book'}), 500)