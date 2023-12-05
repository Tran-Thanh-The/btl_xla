from flask import render_template, flash, Blueprint, request
import cv2
import base64
import os
import numpy as np

gamma_bp = Blueprint("gamma", __name__)

@gamma_bp.route("/gamma", methods=["POST", "GET"])
def gamma():
    if request.method == "POST":
        try:
            image = request.files["image"]
            print(image.filename)

            image.save("images/" + image.filename)
            originalImage = cv2.imread("images/" + image.filename)

            image_float = np.float32(originalImage)
            max_value = np.max(image_float)

            gamma = 0.5

            processedImage = np.uint8(
                np.clip((image_float / max_value) ** gamma * 255.0, 0, 255)
            )

            if not os.path.exists("images/" + image.filename.split(".")[0]):
                os.makedirs("images/" + image.filename.split(".")[0])

            cv2.imwrite(
                "images/" + image.filename.split(".")[0] + "/gamma.jpg",
                processedImage,
            )

            with open("images/" + image.filename, "rb") as img:
                originalImage = base64.b64encode(img.read()).decode("utf-8")

            with open(
                "images/" + image.filename.split(".")[0] + "/gamma.jpg", "rb"
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
