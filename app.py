from flask import Flask, request, render_template, url_for
from facemorph import process_image
import os
import cv2

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    message = None  # Message to display for feedback
    if request.method == "POST":
        if "file" not in request.files:
            message = "No file part in the request."
        else:
            file = request.files["file"]
            if file.filename == "":
                message = "No file selected. Please choose an image to upload."
            elif file:
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)
                avg_image = process_image(file_path)
                result_path = os.path.join(RESULT_FOLDER, "result.jpg")
                cv2.imwrite(result_path, avg_image)
                # Render the page with images
                return render_template(
                    "upload.html",
                    original_image=file.filename,
                    transformed_image="result.jpg",
                    message=None,
                )
    return render_template("upload.html", original_image=None, transformed_image=None, message=message)

if __name__ == "__main__":
    app.run(debug=True)
