from flask import Flask, request  # importeer de Flask class
from flask_cors import CORS
import requests

steamAPIKey = "A862570CC2139926066420C4E9A5A927"

app = Flask(__name__)  # maak een instantie van de Flask class
CORS(app)

# --

# voorbeeld van een route


@app.route("/")  # maak een route naar de index pagina
def hello_world():  # maak een functie die de index pagina weergeeft
    # geef als output een paragraaf met de tekst "Hello, World!"
    return "<p>Hello, World!</p>"

# --


@app.route("/test")  # maak een route naar een test pagina
def test():  # maak een functie die de test pagina weergeeft
    # geef als output json data
    return {"text": "Dit is een stukje data uit het app.py bestand :)"}


@app.route("/api")
def api():
    steamID = request.args.get("steamID")

    session = requests.Session()
    infile = session.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" +
                         steamAPIKey + "&steamids=76561198000000000")
    data = infile.json()

    firstname = data["response"]["players"][0]["personaname"]
    return {"name": firstname}
