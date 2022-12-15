from flask import Flask, request  # importeer de Flask class
from flask_cors import CORS
import requests
import json

steamAPIKey = "A862570CC2139926066420C4E9A5A927"

app = Flask(__name__)  # maak een instantie van de Flask class
CORS(app)

# ---------------------------- ROUTES ---------------------------- #


@app.route("/")  # maak een route naar de index pagina
def hello_world():  # maak een functie die de index pagina weergeeft
    # geef als output een paragraaf met de tekst "Hello, World!"
    return "<p>Home pagina van de Flask Back-end voor Project Steam</p>"


@app.route("/api/getplayersummaries")  # maak een route naar de summary api
def playersum():
    # haal de steamID op uit de url
    steamID = request.args.get("steamID")

    url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}&format=json".format(
        steamAPIKey, steamID)

    # haal de data op
    session = requests.Session()
    infile = session.get(url)
    data = infile.json()

    firstPlayer = data["response"]["players"][0]
    return firstPlayer


@app.route("/api/getfriendlist")  # maak een route naar de friendlist api
def friendlist():
    # haal de steamID op uit de url
    steamID = request.args.get("steamID")

    url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={}&steamid={}&relationship=friend".format(
        steamAPIKey, steamID)

    # haal de data op
    session = requests.Session()
    infile = session.get(url)
    data = infile.json()

    return data


@app.route("/api/loadjson")
def loadJson():  # route wordt gebruikt om de blocktypes op te halen
    # haal de data op uit blockTypes.json
    f = open(app.root_path+"/steam.json")
    data = json.load(f)
    return data


@app.route("/blocktypes")
def blocktypes():  # route wordt gebruikt om de blocktypes op te halen
    # haal de data op uit blockTypes.json
    path = app.root_path + "/blockTypes.json"
    infile = open(path, "r")
    data = infile.read()
    infile.close()

    return data
