import os 

from flask import Flask, render_template, jsonify, request, Response
from flask_pymongo import PyMongo

from flask_app.utils import validate_information_mediator_header, JSONEncoderCustom


app = Flask(__name__)


MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/mydatabase")
app.config["MONGO_URI"] = MONGO_URI

# Initialize MongoDB with Flask App
mongo = PyMongo(app)
db = mongo.db


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data/<registryname>/<versionnumber>/create', methods=['POST'])
def create_record(registryname, versionnumber):
    # Extract header value
    client_header = request.headers.get('Information-Mediator-Client')
    if not client_header:
        return jsonify({"error": "Information-Mediator-Client header missing"}), 400

    client_header_valid = validate_information_mediator_header(client_header)
    if not client_header_valid['success']:
        return jsonify(client_header_valid), 403

    # Validate the body
    data = request.json.get('write', {}).get('content')
    if not data:
        return jsonify({"error": "Invalid request body"}), 400
    # Save the record to MongoDB
    collection = db[registryname]  # Using registryname as the collection name for this example
    collection.insert_one(data)

    data.pop('_id')
    
    response = Response(
        JSONEncoderCustom().encode({'content': data}),
        mimetype="application/json"
    )
    response.headers['Content-Type'] = 'application/json; charset=utf-8'  # setting the content-type header explicitly
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
