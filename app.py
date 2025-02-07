# pip install flask
from io import BytesIO

import numpy as np
from flask import Flask, request, jsonify, send_from_directory
# pip install requests
import requests
# pip install numpy
import numpy as np
# pip install opencv-python
import cv2

import os
from urllib.parse import urlparse

# pip install python-dotenv
from dotenv import load_dotenv

# Load .env file
load_dotenv()


# modules
import processing


app = Flask(__name__)

# Define the directory for processed images
PROCESSED_DIR = "processed_images"
os.makedirs(PROCESSED_DIR, exist_ok=True)  # Ensure the folder exists

@app.route("/processing", methods=["POST"])
def process_images():
    try:

        # extract JSON payload
        data = request.json
        if not data or "file" not in data:
            return jsonify({"error" : "No file URL provided"}), 400

        file_url = data['file']

        # fetch the image from the provided URL
        # response = requests.get(file_url)
        response = requests.get(file_url, headers={"User-Agent" : "Mozilla/5.0"})

        if response.status_code != 200:
            return jsonify({"error": f"Failed to fetch image. Status: {response.status_code}"}), 400


        # Detect the file extension from Content-Type
        content_type = response.headers.get("Content-Type", "")
        if "image/png" in content_type:
            ext = ".png"
        elif "image/jpeg" in content_type or "image/jpg" in content_type:
            ext = ".jpg"
        else:
            return {"error": f"Unsupported image type: {content_type}"}

        # Convert the response content to a NumPy array for OpenCV
        image_array = np.frombuffer(response.content, np.uint8)
        img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({"error": "Invalid image format"}), 400

        # Extract the filename from the URL
        # filename = os.path.basename(urlparse(file_url).path)

        # Generate a filename
        filename = os.path.basename(urlparse(file_url).path) or "image"
        filename += ext  # Add detected extension

        # Process the image using your function
        result = processing.adjustImages(img)  # Ensure this function works properly

        # Save the image using the extracted filename
        save_path = os.path.join("processed_images", filename)  # Save in processed_images folder
        os.makedirs("processed_images", exist_ok=True)  # Ensure directory exists
        cv2.imwrite(save_path, result)

        # result full path
        processed_path = f"{os.getenv('APP_URL')}/processed_images/{filename}"

        return jsonify({"message": "Processing successful", "result" : processed_path})

    except Exception as e:
        return jsonify({"error" : str(e)}), 500


# Serve processed images
@app.route("/processed_images/<filename>", methods=["GET"])
def processed_images(filename):
    return send_from_directory(PROCESSED_DIR, filename)


# run server
if __name__ == "__main__":
    app.run(debug=True)