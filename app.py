import json
from pprint import pprint

from flask import Flask, request

from util import get_api_key

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.post("/omnivore-webhook")
def omnivore_webhook():
    with open("content.json", "wb") as f:
        f.write(request.data)
    # with open("headers.json", "wb") as f:
    #     json.dump(dict(request.headers), f)
    pprint(dict(request.headers))
    print()
    pprint(json.loads(request.data))
    print()
    return {
        # "foo": "bar",
        # "headers": request.headers,
        # "data": request.data,
        "status": "cool",
    }
