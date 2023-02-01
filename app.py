from flask import Flask, request  # importeer de Flask class
from flask_cors import CORS
import mysql.connector
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

    if (data["response"]["players"] == []):
        return "no-data"

    firstPlayer = data["response"]["players"][0]
    returnData = firstPlayer

    # check of het argument variable is doorgegeven, zo ja, haal dan alleen die data op
    variable = request.args.get("variable")
    if variable is not None:
        returnData = firstPlayer[variable]

    return returnData


@app.route("/api/onlineplayers")
def online():
    # haal de steamids uit de url
    steamids = request.args.get("steamIDs")
    url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}&format=json".format(
        steamAPIKey, steamids)

    # haal de data op
    session = requests.Session()
    infile = session.get(url)
    data = infile.json()
    players = data["response"]["players"]

    if (players == []):
        return "no-data"

    onplayers = []
    for player in players:
        if player['personastate'] == 1:
            onplayers.append(player['realname'])

    return json.dumps(onplayers)


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


@app.route("/api/getrecentlyplayedgames")
def recentlyplayedgames():
    # haal de steamID op uit de url
    steamID = request.args.get("steamID")

    url = "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={}&steamid={}&format=json".format(
        steamAPIKey, steamID)

    # haal de data op
    session = requests.Session()
    infile = session.get(url)
    data = infile.json()

    return data

# route wordt gebruikt om de doorgegeven json file op te halen


@app.route("/api/loadjson")
def loadJson():  # route wordt gebruikt om de blocktypes op te halen
    # haal de limiet op uit de url
    limiet = request.args.get("limit")

    # haal de offset op uit de url
    offset = request.args.get("offset")
    # als offset niet is doorgegeven, zet hem dan op 0
    if offset is None:
        offset = 0

    # haal de data op uit blockTypes.json
    f = open(app.root_path+"/steam.json")
    data = json.load(f)

    # haal de lengte van het originele bestand op
    dataLen = len(data)

    # als er een limiet is opgegeven, haal dan alleen die data op
    if limiet is not None:
        data = data[int(offset):int(limiet)+int(offset)]

    # return de data en de lengte van het originele bestand
    return {"data": data, "originalLength": dataLen}


# route wordt gebruikt om de blockSaved.json op te halen
@app.route("/api/blocksaved")
def blocksaved():
    # haal de steamID op uit de url
    steamID = request.args.get("steamID")

    # haal de data op uit blockSaved.json
    f = open(app.root_path+"/blockSaved.json")
    data = json.load(f)

    # haal het juiste item op uit de list door de steamID
    for item in data:
        if item["steamID"] == steamID:
            return item

    # return een lege json als er geen item is gevonden, eerste item in json is leeg
    return data[0]


# route wordt gebruikt om de blockSaved.json te updaten
@app.route("/api/blocksave", methods=["POST"])
def blocksave():
    # haal de data op uit de request
    data = request.get_json()

    # haal de data op uit blockSaved.json
    f = open(app.root_path+"/blockSaved.json")
    savedData = json.load(f)

    # als de steamID niet in de lijst staat, voeg hem dan toe
    if not any(item["steamID"] == data["steamID"] for item in savedData):
        savedData.append(data)

    # haal het juiste item op uit de list door de steamID
    for item in savedData:
        if item["steamID"] == data["steamID"]:
            item["blocks"] = data["blocks"]
            break

    # schrijf de data terug naar blockSaved.json
    f = open(app.root_path+"/blockSaved.json", "w")
    json.dump(savedData, f)

    return "Success"


@app.route("/blocktypes")
def blocktypes():  # route wordt gebruikt om de blocktypes op te halen
    # haal de data op uit blockTypes.json
    path = app.root_path + "/blockTypes.json"
    infile = open(path, "r")
    data = infile.read()
    infile.close()

    return data


@app.route("/api/blockSearch")
def search():
    # haal de zoekterm op uit de url
    searchterm = request.args.get("searchterm")

    # haal de namen op uit de url
    names = request.args.get("names")

    # sorteer de namen op alfabet
    names = names.split(",")
    names = mergeSort(names, searchterm)

    # geef de gesorteerde namen terug, en als de score 0 is, haal de naam dan uit de lijst
    names = [name for name in names if nameCompare(name, searchterm) > 0]

    print(names)

    # zoek de namen op de zoekterm
    # names = searchNames(names, searchterm)

    return json.dumps(names)


def mergeSort(names, term):
    # sorteer de namen op compare score met de zoekterm
    if len(names) > 1:
        mid = len(names)//2
        left = names[:mid]
        right = names[mid:]

        mergeSort(left, term)
        mergeSort(right, term)

        i = j = k = 0

        while i < len(left) and j < len(right):
            if nameCompare(left[i], term) > nameCompare(right[j], term):
                names[k] = left[i]
                i += 1
            else:
                names[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            names[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            names[k] = right[j]
            j += 1
            k += 1

    return names


def nameCompare(name, term):
    # vergelijk de naam met de zoekterm, en return een score op basis van de overeenkomsten
    score = 0

    # als de naam begint met de zoekterm, geef dan een hogere score
    if name.startswith(term):
        score += 10

    # als de naam de zoekterm bevat, geef dan een hogere score
    if term in name:
        score += 5

    # als de naam de zoekterm bevat, geef dan een hogere score
    if term.lower() in name.lower():
        score += 2

    # als de naam de zoekterm bevat, geef dan een hogere score
    if term.upper() in name.upper():
        score += 1

    return score


@app.route("/pico")
def picodata():
    path = app.root_path + "/Hardware/picoData.json"
    f = open(path, "r")
    data = json.load(f)
    return data

@app.route("/db/afktijd")
def afktijd():
    steamID = request.args.get("steamID")


    db = mysql.connector.connect(
        host="sql7.freemysqlhosting.net",
        user="sql7594625",
        passwd="KVtzBMv5fB",
        db="sql7594625"
    )
    c = db.cursor()
    query = "SELECT afktijd FROM sessie\n" \
            "WHERE gebruikersteamid = {};".format(steamID)
    if steamID is None:
        return "Geef steam id"

    c.execute(query)
    data = c.fetchall()
    c.close()
    db.close()
    return data

@app.route("/db/watergedronken")
def watergedronken():
    steamID = request.args.get("steamID")


    db = mysql.connector.connect(
        host="sql7.freemysqlhosting.net",
        user="sql7594625",
        passwd="KVtzBMv5fB",
        db="sql7594625"
    )
    c = db.cursor()
    query = "SELECT watergedronken FROM sessie\n" \
            "WHERE gebruikersteamid = {};".format(steamID)
    if steamID is None:
        return "Geef steam id"

    c.execute(query)
    data = c.fetchall()
    c.close()
    db.close()
    return data


