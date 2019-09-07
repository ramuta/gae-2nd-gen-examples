from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    name = "SmartNinja"
    return render_template("index.html", name=name)


if __name__ == '__main__':
    app.run(port=8080, host="localhost")
