import os
import json
import redis
import requests
from flask import Flask
from dotenv import load_dotenv

# Loads the .env file🔐
load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

r = redis.Redis(host=os.getenv('HOSTNAME'), port=os.getenv('PORT'), db=0)


@app.route("/repo/<username>")
def main(username):
    # Get the data from github API⚡
    BaseUrl = requests.get(f"https://api.github.com/users/{username}")
    data = BaseUrl.json()

    # Set data to redis🛢
    r.set('data', json.dumps(data))

    # Get data from redis🛢
    data = r.get('data')

    data = json.loads(data)
    return f"<h3>{data['name']} has {data['public_repos']} public repositories</h3>"


if __name__ == "__main__":
    app.run(debug=True)
