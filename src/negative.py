from flask import render_template, flash, Blueprint, request
import cv2
import base64
import os

negative_bp = Blueprint("negative", __name__)

@IP.route("/negative", methods=["GET", "POST"])
def negative():
    if request.method == "POST":
        try:
            image = request.files["image"]
            print(image.filename)
            
            image.save("images/" + image.filename)
            originalImage = cv2.imread("images/" + image.filename)

            processedImage = cv2.bitwise_not(originalImage)

            if not os.path.exists("images/" + image.filename.split(".")[0]):
                os.makedirs("images/" + image.filename.split(".")[0])

            cv2.imwrite(
                "images/" + image.filename.split(".")[0] + "/inverted.jpg",
                processedImage,
            )

            with open("images/" + image.filename, "rb") as img:
                originalImage = base64.b64encode(img.read()).decode("utf-8")

            with open(
                "images/" + image.filename.split(".")[0] + "/inverted.jpg", "rb"
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
