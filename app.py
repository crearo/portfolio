from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('basic_home.html')


if __name__ == "__main__":
    print("running py app")
    app.run(host="127.0.0.1", port=5000, debug=True)
