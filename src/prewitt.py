from flask import render_template, flash, Blueprint, request
import cv2
import base64
import os

prewitt_bp = Blueprint("prewitt", __name__)

@prewitt_bp.route("/prewitt", methods=["POST", "GET"])
def prewitt():
    if request.method == "POST":
        try:
            image = request.files["image"]
            print(image.filename)

            image.save("images/" + image.filename)
            originalImage = cv2.imread("images/" + image.filename)

            gray_image = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)

            prewitt_kernel_x = cv2.getDerivKernels(1, 0, 3, normalize=True)
            prewitt_kernel_y = cv2.getDerivKernels(0, 1, 3, normalize=True)
            prewitt_x = cv2.filter2D(
                gray_image, cv2.CV_64F, prewitt_kernel_x[0] * prewitt_kernel_x[1]
            )
            prewitt_y = cv2.filter2D(
                gray_image, cv2.CV_64F, prewitt_kernel_y[0] * prewitt_kernel_y[1]
            )

            processedImage = cv2.magnitude(prewitt_x, prewitt_y)

            if not os.path.exists("images/" + image.filename.split(".")[0]):
                os.makedirs("images/" + image.filename.split(".")[0])

            cv2.imwrite(
                "images/" + image.filename.split(".")[0] + "/prewitt.jpg",
                processedImage,
            )

            with open("images/" + image.filename, "rb") as img:
                originalImage = base64.b64encode(img.read()).decode("utf-8")

            with open(
                "images/" + image.filename.split(".")[0] + "/prewitt.jpg", "rb"
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
