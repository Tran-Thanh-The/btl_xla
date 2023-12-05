from flask import render_template, flash, Blueprint, request
import cv2
import base64
import os
import numpy as np

logarith_bp = Blueprint("logarith", __name__)

@logarith_bp.route("/logarith", methods=["POST", "GET"])
def logarith():
    if request.method == "POST":
        try:
            image = request.files["image"]
            print(image.filename)

            image.save("images/" + image.filename)
            originalImage = cv2.imread("images/" + image.filename)

            image_float = np.float32(originalImage)

            c = 255 / np.log(1 + np.max(image_float))
            log_image = c * (np.log(image_float + 1))

            processedImage = np.uint8(log_image)

            if not os.path.exists("images/" + image.filename.split(".")[0]):
                os.makedirs("images/" + image.filename.split(".")[0])

            cv2.imwrite(
                "images/" + image.filename.split(".")[0] + "/logarith.jpg",
                processedImage,
            )

            with open("images/" + image.filename, "rb") as img:
                originalImage = base64.b64encode(img.read()).decode("utf-8")

            with open(
                "images/" + image.filename.split(".")[0] + "/logarith.jpg", "rb"
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
