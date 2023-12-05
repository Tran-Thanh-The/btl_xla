from flask import render_template, flash, Blueprint, request
import cv2
import base64
import os
import numpy as np

roberts_bp = Blueprint("roberts", __name__)

@roberts_bp.route("/roberts", methods=["POST", "GET"])
def roberts():
    if request.method == "POST":
        try:
            image = request.files["image"]
            print(image.filename)

            image.save("images/" + image.filename)
            originalImage = cv2.imread("images/" + image.filename)

            gray_image = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)

            roberts_x = np.array([[1, 0], [0, -1]], dtype=np.float32)
            roberts_y = np.array([[0, -1], [1, 0]], dtype=np.float32)

            roberts_x_edges = cv2.filter2D(gray_image, -1, roberts_x)
            roberts_y_edges = cv2.filter2D(gray_image, -1, roberts_y)

            roberts_x_edges = roberts_x_edges.astype(np.float32)
            roberts_y_edges = roberts_y_edges.astype(np.float32)

            processedImage = cv2.magnitude(roberts_x_edges, roberts_y_edges)

            if not os.path.exists("images/" + image.filename.split(".")[0]):
                os.makedirs("images/" + image.filename.split(".")[0])

            cv2.imwrite(
                "images/" + image.filename.split(".")[0] + "/roberts.jpg",
                processedImage,
            )

            with open("images/" + image.filename, "rb") as img:
                originalImage = base64.b64encode(img.read()).decode("utf-8")

            with open(
                "images/" + image.filename.split(".")[0] + "/roberts.jpg", "rb"
            ) as img:
                processedImage = base64.b64encode(img.read()).decode("utf-8")

            return render_template(
                "index.html",
                originalImage=originalImage,
                processedImage=processedImage,
            )
        except:
            flash("Processing error!", "error")

    return render_template("index.html")
