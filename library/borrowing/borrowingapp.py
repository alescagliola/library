from flask import Flask, request, jsonify, make_response
from pymongo import MongoClient
from bson import ObjectId
from os import environ

app = Flask(__name__)
client = MongoClient(environ.get('MONGO_URI'))
db = client.borrowingservice  # 

@app.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)

@app.route('/borrowing', methods=['POST'])
def new_loan():
    try:
        data = request.get_json()
        result = db.borrowings.insert_one(data)
        return make_response(jsonify({'message': 'loan added', 'id': str(result.inserted_id)}), 201)
    except Exception as e:
        print(str(e))
        return make_response(jsonify({'message': 'error adding the loan'}), 500)

@app.route('/borrowing', methods=['GET'])
def get_loans():
    try:
        loans = list(db.borrowings.find())
        return make_response(jsonify(loans), 200)
    except Exception as e:
        print(str(e))
        return make_response(jsonify({'message': 'error getting loans'}), 500)

@app.route('/borrowing/<string:id>', methods=['GET'])
def get_loan(id):
    try:
        loan = db.borrowings.find_one({'_id': ObjectId(id)})
        if loan:
            return make_response(jsonify(loan), 200)
        return make_response(jsonify({'message': 'loan not found'}), 404)
    except Exception as e:
        print(str(e))
        return make_response(jsonify({'message': 'error getting the loan'}), 500)

@app.route('/borrowing/<string:id>', methods=['PUT'])
def update_loan(id):
    try:
        data = request.get_json()
        result = db.borrowings.update_one({'_id': ObjectId(id)}, {'$set': data})
        if result.modified_count > 0:
            return make_response(jsonify({'message': 'loan updated'}), 200)
        return make_response(jsonify({'message': 'loan not found'}), 404)
    except Exception as e:
        print(str(e))
        return make_response(jsonify({'message': 'error updating the loan'}), 500)

@app.route('/borrowing/<string:id>', methods=['DELETE'])
def delete_loan(id):
    try:
        result = db.borrowings.delete_one({'_id': ObjectId(id)})
        if result.deleted_count > 0:
            return make_response(jsonify({'message': 'loan deleted'}), 200)
        return make_response(jsonify({'message': 'loan not found'}), 404)
    except Exception as e:
        print(str(e))
        return make_response(jsonify({'message': 'error deleting the loan'}), 500)

if __name__ == '__main__':
    app.run(debug=True)
