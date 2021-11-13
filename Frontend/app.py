from flask import Flask
from flask import request, redirect, render_template, session
import requests

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route('/pipe', methods=["GET", "POST"])
def pipe():
    data = request.form.get("data")
    payload = {}
    headers = {}
    # change the url to "http://127.0.0.1:4000/autocomplete?query=" to run the backend locally
    url = "http://backend:4000/autocomplete?query=" + str(data)
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.json())
    return response.json()


@app.route('/translate', methods=["GET", "POST"])
def translate():
    data = request.form.get("data")
    print(data)
    return data


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
