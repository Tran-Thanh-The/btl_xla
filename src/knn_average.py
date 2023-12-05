from flask import render_template, flash, Blueprint, request
import cv2
import base64
import os
import numpy as np

knn_average_bp = Blueprint("knn_average", __name__)

def knn_filter(image, k):
    kernel = np.ones((k, k), dtype=np.float32) / (
        k * k
    )

    filtered_image = cv2.filter2D(image, -1, kernel)

    return filtered_image

@knn_average_bp.route("/knn_average", methods=["POST", "GET"])
def knn_average():
    if request.method == "POST":
        try:
            image = request.files["image"]
            print(image.filename)

            image.save("images/" + image.filename)
            originalImage = cv2.imread("images/" + image.filename)

            processedImage = knn_filter(originalImage, 3)

            if not os.path.exists("images/" + image.filename.split(".")[0]):
                os.makedirs("images/" + image.filename.split(".")[0])

            cv2.imwrite(
                "images/" + image.filename.split(".")[0] + "/knn_average.jpg",
                processedImage,
            )

            with open("images/" + image.filename, "rb") as img:
                originalImage = base64.b64encode(img.read()).decode("utf-8")

            with open(
                "images/" + image.filename.split(".")[0] + "/knn_average.jpg",
                "rb",
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
