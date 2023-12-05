from flask import render_template, flash, Blueprint, request
import cv2
import base64
import os

canny_bp = Blueprint("canny", __name__)

@canny_bp.route("/canny", methods=["POST", "GET"])
def canny():
    if request.method == "POST":
        try:
            image = request.files["image"]
            print(image.filename)

            image.save("images/" + image.filename)
            originalImage = cv2.imread("images/" + image.filename)

            gray_image = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)

            blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

            processedImage = cv2.Canny(
                blurred_image, 50, 150
            )

            if not os.path.exists("images/" + image.filename.split(".")[0]):
                os.makedirs("images/" + image.filename.split(".")[0])

            cv2.imwrite(
                "images/" + image.filename.split(".")[0] + "/canny.jpg",
                processedImage,
            )

            with open("images/" + image.filename, "rb") as img:
                originalImage = base64.b64encode(img.read()).decode("utf-8")

            with open(
                "images/" + image.filename.split(".")[0] + "/canny.jpg", "rb"
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
