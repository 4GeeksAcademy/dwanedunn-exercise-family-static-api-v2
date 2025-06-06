"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")
# initial_data = [
#     {
#         "first_name": "John",
#         "last_name": "Jackson",
#         "age": 33,
#         "lucky_numbers": [7, 13, 22]
#     },
#     {
#         "first_name": "Jane",
#         "last_name": "Jackson",
#         "age": 35,
#         "lucky_numbers": [10, 14, 3]
#     },
#     {
#         "first_name": "Jimmy",
#         "last_name": "Jackson",
#         "age": 5,
#         "lucky_numbers": [1]
#     }
# ]
# for members_data in initial_data:
#     jackson_family.add_member(members_data)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200

@app.route('/members', methods=['POST'])
def add_member():
    body = request.get_json()
    if body is None:
        return jsonify({"msg": "bad request"}), 400,
    jackson_family.add_member(body)
    return jsonify({"msg": "member added successfully"}), 200

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
