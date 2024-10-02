from flask import Flask, request, jsonify, send_file
from flask_cors import CORS


app = Flask(__name__)
app.debug = True
CORS(app)

import backend.routes

# @app.route("/", methods=["GET"])
# def landing_page():
#     return jsonify(message="Landing page")
