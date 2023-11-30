from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from sqlalchemy import Date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class Borrowing(db.Model):
    __tablename__ = 'borrowing'

    id = db.Column(db.Integer, primary_key=True)
    loandate = db.Column(Date, nullable=False)
    returndate = db.Column(Date, nullable=False)
    clientid = db.Column(db.Integer)
    bookid = db.Column(db.Integer)

    def json(self):
        return {'id': self.id, 'loandate': self.loandate, 'returndate': self.returndate, 'clientid': self.clientid, 'bookid': self.bookid}

db.create_all()


@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route'}), 200)


@app.route('/borrowing', methods=['POST'])
def new_loan():
  try:
    data = request.get_json()
    new_loan = Borrowing(id=data['id'], loandate=data['loandate'], returndate=data['returndate'], clientid=data['clientid'], bookid=data['bookid'])
    db.session.add(new_loan)
    db.session.commit()
    return make_response(jsonify({'message': 'loan added'}), 201)
  except Exception as e:
    print(str(e))
    return make_response(jsonify({'message': 'error adding the loan'}), 500)


@app.route('/borrowing', methods=['GET'])
def get_loans():
  try:
    loans = Borrowing.query.all()
    return make_response(jsonify([loan.json() for loan in loans]), 200)
  except Exception as e:
    print(str(e))
    return make_response(jsonify({'message': 'error getting loans'}), 500)


@app.route('/borrowing/<int:id>', methods=['GET'])
def get_loan(id):
  try:
    loan = Borrowing.query.filter_by(id=id).first()
    if loan:
      return make_response(jsonify({'user': loan.json()}), 200)
    return make_response(jsonify({'message': 'loan not found'}), 404)
  except Exception as e:
    print(str(e))
    return make_response(jsonify({'message': 'error getting the loan'}), 500)


@app.route('/borrowing/<int:id>', methods=['PUT'])
def update_loan(id):
  try:
    loan = Borrowing.query.filter_by(id=id).first()
    if loan:
      data = request.get_json()
      loan.loandate = data['loandate']
      loan.returndate = data['returndate']
      loan.clientid = data['clientid']
      loan.bookid = data['bookid']
      db.session.commit()
      return make_response(jsonify({'message': 'loan updated'}), 200)
    return make_response(jsonify({'message': 'loan not found'}), 404)
  except Exception as e:
    print(str(e))
    return make_response(jsonify({'message': 'error updating the loan'}), 500)


@app.route('/borrowing/<int:id>', methods=['DELETE'])
def delete_loan(id):
  try:
    loan = Borrowing.query.filter_by(id=id).first()
    if loan:
      db.session.delete(loan)
      db.session.commit()
      return make_response(jsonify({'message': 'loan deleted'}), 200)
    return make_response(jsonify({'message': 'loan not found'}), 404)
  except Exception as e:
    print(str(e))
    return make_response(jsonify({'message': 'error deleting the loan'}), 500)