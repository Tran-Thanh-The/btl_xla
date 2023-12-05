from flask import Flask, redirect, render_template
from ImageProcessing import IP

app = Flask(__name__)
app.config["SECRET_KEY"] = "00000000"
app.register_blueprint(IP)


@app.route("/")
def home():
    return render_template("main.html")


if __name__ == "__main__":
    app.run(debug=True)
