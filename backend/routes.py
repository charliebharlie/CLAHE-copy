import os
import numpy as np
import io
import uuid
import base64
import pickle
from . import app
from clahe import main

from flask import Flask, request, jsonify, send_file
from PIL import Image

PROXIES = {
    "http": None,
    "https": None,
}

DATABASE_FILE_PATH = "./database/database.pkl"


def save_database(database, file_path):
    with open(file_path, "wb") as file:
        pickle.dump(database, file)


def load_database(file_path):
    try:
        with open(file_path, "rb") as file:
            database = pickle.load(file)
    except Exception as e:
        database = {}
        print(str(e))

    return database


def add_image_to_database(database, image_name, image_data):
    database[image_name] = image_data
    save_database(database, DATABASE_FILE_PATH)


images = load_database(DATABASE_FILE_PATH)


@app.route("/", methods=["GET"])
def landing_page():
    return jsonify(message="Test")


@app.route("/test", methods=["POST"])
def test():
    print("Success")
    return jsonify(message="Successfully posted")


@app.route("/user_upload_image", methods=["POST"])
def user_upload_image():
    global images
    # Access the uploaded file from the request
    try:
        if "file" not in request.files:
            return {"error": "No file part"}, 400

        file = request.files["file"]

        if file.filename == "":
            return {"error": "No selected file"}, 400

        file_path = f"uploads/{file.filename}"

        # Save the uploaded file to a directory
        file.save(file_path)
        print(file)
        main.run_algorithms(file_path, 2, 2, 10)
        print("----------------------------------------------------")
        return jsonify(success=True, message="Image uploaded successfully"), 200

    except Exception as e:
        None
        return (
            jsonify(success=False, message="Error occured while uploading image"),
            400,
        )


@app.route("/algorithm_upload_images", methods=["POST"])
def algorithm_upload_images():
    global images
    if "image" not in request.files:
        return jsonify(error="No image file provided"), 404

    image_file = request.files["image"]
    if image_file.filename == "":
        return jsonify(error="No selected file"), 404

    try:
        image_name = image_file.filename
        image_file = Image.open(image_file.stream)
        image = np.array(image_file)
        image_id = str(uuid.uuid4())

        image_data = {"image": image, "image_id": image_id}
        images[image_name] = image_data
        add_image_to_database(images, image_name, image_data)

        return jsonify(
            success=True,
            message="Image uploaded successfully",
            id=image_id,
            name=image_name,
        )

    except Exception as e:
        return jsonify(error=f"Error processing image: {str(e)}"), 500


@app.route("/get_image_data", methods=["GET"])
def get_image_data():
    global images
    response_data = {}
    if not images:
        return jsonify(error="Images not found"), 404

    for image_name in images:
        try:
            image = images[image_name]
            image_id = image["image_id"]
            image_array = image["image"]

            # Convert Numpy array to PIL image
            image = Image.fromarray(image_array.astype("uint8"))

            # Create an empty binary stream in memory
            img_io = io.BytesIO()
            # Saves the image into the binary stream
            image.save(img_io, "PNG")

            # Convert to base64
            img_str = base64.b64encode(img_io.getvalue()).decode("utf-8")

            # Add to response data
            response_data[image_name] = {
                "id": image_id,  # Assuming you store ID in image_info
                "image": img_str,
            }
            # Ensures that the file pointer starts at the beginning of the image
            # img_io.seek(0)

            # send the in-memory file object as a PNG image
            # return send_file(img_io, mimetype="image/png")
        except Exception as e:
            return jsonify(error=f"Error serving image: {str(e)}"), 500
    return jsonify(response_data)


@app.route("/clear_images", methods=["POST"])
def clear_images():
    global images

    try:
        # Opening a file clears it in python
        with open(DATABASE_FILE_PATH, "w") as file:
            if images:
                pass
            else:
                return jsonify(message="No images to clear!"), 404
        images = load_database(DATABASE_FILE_PATH)
    except Exception as e:
        return jsonify({"message": "An error occurred while clearing images"}), 500

    return jsonify(message="Cleared images")


# TODO: FIx this
# @app.route("/adjust_curve/<curve_id>", methods=["POST"])
# def adjust_curve(image_id):
#     global images
#     if image_id not in images:
#         return jsonify(error="Image not found"), 404
#
#     try:
#         data = request.json
#         return jsonify(success=True, message="Curve applied successfully")
#     except Exception as e:
#         return jsonify(error=f"Error adjusting curve: {str(e)}"), 500
