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

    # haal de status van de vrienden op via de getplayersummaries api
    # maak een lijst met de steamIDs van de vrienden
    friends = data["friendslist"]["friends"]
    steamIDs = ""
    for friend in friends:
        steamIDs += friend["steamid"] + ","
    steamIDs = steamIDs[:-1]

    # haal de data op van de getplayersummaries api
    url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}&format=json".format(
        steamAPIKey, steamIDs)

    # haal de data op
    session = requests.Session()
    infile = session.get(url)
    playerData = infile.json()

    # zet de status van de vrienden in de data van de vrienden
    for friend in friends:
        for player in playerData["response"]["players"]:
            if friend["steamid"] == player["steamid"]:
                friend["status"] = player["personastate"]

    # return de data
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

    currentFilter = request.args.get("filter")
    if currentFilter is None:
        currentFilter = "10000"  # als er geen filter is doorgegeven, zet hem dan op 10000

    # haal de data op uit blockTypes.json
    f = open(app.root_path+"/steam.json")
    data = json.load(f)

    # haal alle items waarbij de prijs lager is dan currentFilter, waarbij de prijs staat in de key "price"
    data = [item for item in data if item["price"] <= int(currentFilter)]

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


@app.route("/api/afktijd")
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

    dataList = []
    # haal de data uit de tuples en voeg ze toe aan dataList
    for item in data:
        dataList.append(item[0])

    return {
        "sessions": dataList,
        "mean": mean(dataList),
        "range": rnge(dataList),
        "median": median(dataList),
        "q1": q1(dataList),
        "q3": q3(dataList),
        "var": var(dataList),
        "std": std(dataList),
        "modes": modes(dataList)
    }


@app.route("/api/watergedronken")
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

    dataList = []
    # haal de data uit de tuples en voeg ze toe aan dataList
    for item in data:
        dataList.append(item[0])

    return {
        "sessions": dataList,
        "mean": mean(dataList),
        "range": rnge(dataList),
        "median": median(dataList),
        "q1": q1(dataList),
        "q3": q3(dataList),
        "var": var(dataList),
        "std": std(dataList),
        "modes": modes(dataList)
    }


@app.route("/api/jsonpricestats")
def jsonPriceStats():
    # haal de json data op met de json, en haal alleen de prijzen eruit
    # haal de data op uit blockTypes.json
    f = open(app.root_path+"/steam.json")
    data = json.load(f)

    # haal de prijzen eruit
    prices = [item["price"] for item in data]

    # maak een dictionary aan met de statistieken
    stats = {
        "mean": mean(prices),
        "range": rnge(prices),
        "median": median(prices),
        "q1": q1(prices),
        "q3": q3(prices),
        "var": var(prices),
        "std": std(prices),
        "freq": freq(prices),
        "modes": modes(prices)
    }

    # geef de statistieken terug
    return stats


@app.route("/api/jsonreviewstats")
def jsonReviewStats():
    # haal de json data op met de json, en haal alleen de prijzen eruit
    # haal de data op uit blockTypes.json
    f = open(app.root_path+"/steam.json")
    data = json.load(f)

    # haal de positieve / negatieve reviews eruit
    positive = [item["positive_ratings"] for item in data]
    negative = [item["negative_ratings"] for item in data]

    # maak een score tussen 0 en 100 van de reviews, waar 0 = 0% positief, en 100 = 100% positief
    reviews = [round((positive[i] / (positive[i] + negative[i])) * 100)
               for i in range(len(positive))]

    # maak een dictionary aan met de statistieken
    stats = {
        "mean": mean(reviews),
        "range": rnge(reviews),
        "median": median(reviews),
        "q1": q1(reviews),
        "q3": q3(reviews),
        "var": var(reviews),
        "std": std(reviews),
        "modes": modes(reviews),
        "div": {
            "positive": positive,
            "negative": negative
        }
    }

    # geef de statistieken terug
    return stats

# ------------------------------------
# STATISTIEK FUNCTIES - UIT FA3
# ------------------------------------


@app.route("/api/statistiek")
def statistiek():
    # haal de functie op uit de url
    functie = request.args.get("functie")

    # haal de data op uit de url
    data = request.args.get("data")
    data = data.split(",")  # split de data op komma's

    # zet de data om naar integers
    data = [int(item) for item in data]

    # roep de functie aan
    if functie == "mean":
        return str(mean(data))
    elif functie == "range":
        return str(rnge(data))
    elif functie == "median":
        return str(median(data))
    elif functie == "q1":
        return str(q1(data))
    elif functie == "q3":
        return str(q3(data))
    elif functie == "var":
        return str(var(data))
    elif functie == "std":
        return str(std(data))
    elif functie == "freq":
        return str(freq(data))
    elif functie == "modes":
        return str(modes(data))

    return "Geef een geldige functie op"


def mean(lst):
    """
    Bepaal het gemiddelde van een lijst getallen.

    Args:
        lst (list): Een lijst met gehele getallen.

    Returns:
        float: Het gemiddelde van de gegeven getallen.
    """

    # Som van alle getallen gedeeld door het aantal getallen
    return sum(lst) / len(lst)


def rnge(lst):
    """
    Bepaal het bereik van een lijst getallen.

    Args:
        lst (list): Een lijst met gehele getallen.

    Returns:
        int: Het bereik van de gegeven getallen.
    """

    return int(max(lst) - min(lst))  # Grootste getal min het kleinste getal


def median(lst):
    """
    Bepaal de mediaan van een lijst getallen.

    Args:
        lst (list): Een lijst met gehele getallen.

    Returns:
        float: De mediaan van de gegeven getallen.
    """

    lst.sort()
    if (len(lst) % 2 == 0):  # Even aantal getallen
        return float(lst[int(len(lst) / 2)] + lst[int(len(lst) / 2) - 1]) / 2.0
    else:  # Oneven aantal getallen
        return float(lst[int(len(lst) / 2)])


def q1(lst):
    """
    Bepaal het eerste kwartiel Q1 van een lijst getallen.

    Hint: maak gebruik van `median()`

    Args:
        lst (list): Een lijst met gehele getallen.

    Returns:
        float: Het eerste kwartiel Q1 van de gegeven getallen.
    """

    lst.sort()
    # Vanaf de eerste waarde tot de eerste waarde in de tweede helft
    return median(lst[:int(len(lst) / 2)])


def q3(lst):
    """
    Bepaal het derde kwartiel Q3 van een lijst getallen.

    Args:
        lst (list): Een lijst met gehele getallen.

    Returns:
        float: Het derde kwartiel Q3 van de gegeven getallen.
    """

    lst.sort()
    # Index van de eerste waarde in de tweede helft
    fromIndex = int(len(lst) / 2)
    if (len(lst) % 2 != 0):  # Oneven aantal getallen, dus een extra getal in de tweede helft
        fromIndex += 1
    return median(lst[fromIndex:])  # Vanaf de eerste waarde in de tweede helft


def var(lst):
    """
    Bepaal de variantie van een lijst getallen.

    Args:
        lst (list): Een lijst met gehele getallen.

    Returns:
        float: De variantie van de gegeven getallen.
    """

    return sum([(x - mean(lst)) ** 2 for x in lst]) / len(lst)
    # voor elk getal in de lijst, het verschil tussen het getal en het gemiddelde van de lijst (mean)
    # daar het verschil van het kwadraat (**2) van nemen en dat bij elkaar optellen (sum)


def std(lst):
    """
    Bepaal de standaardafwijking van een lijst getallen.

    Args:
        lst (list): Een lijst met gehele getallen.

    Returns:
        float: De standaardafwijking van de gegeven getallen.
    """

    return var(lst) ** 0.5
    # wortel van variantie


def freq(lst):
    """
    Bepaal de frequenties van alle getallen in een lijst.

    Args:
        lst (list): Een lijst met gehele getallen.

    Returns:
        dict: Een dictionary met als 'key' de waardes die voorkomen in de lijst
            en als 'value' het aantal voorkomens (de frequentie) van die waarde.

    Examples:
        >> freq([0, 0, 4, 7, 7])
        {0: 2, 4: 1, 7: 2}

        >> freq([1, 1, 2, 3, 2, 1])
        {1: 3, 2: 2, 3: 1}
    """
    freqs = dict()

    for x in lst:  # Voor elk getal in de lijst
        if x in freqs:  # Als het getal al in de dictionary zit
            freqs[x] += 1  # Tel er 1 bij op
        else:  # Anders
            freqs[x] = 1  # Zet het getal in de dictionary met een waarde van 1

    return freqs  # Geef de dictionary terug


def modes(lst):
    """
    Bepaal alle modi van een lijst getallen.

    Hint: maak gebruik van `freq()`.

    Args:
        lst (list): Een lijst met gehele getallen.

    Returns:
        list: Een gesorteerde lijst van de modi van de gegeven getallen.

    Examples:
        >> modes([0, 0, 4, 7, 7])
        [0, 7]

        >> modes([1, 1, 2, 3, 2, 1])
        [1]
    """
    modi = []

    for x in freq(lst):  # Voor elk getal in de dictionary
        # Als het aantal voorkomens van het getal gelijk is aan het hoogste aantal voorkomens
        if freq(lst)[x] == max(freq(lst).values()):
            modi.append(x)  # Voeg het getal toe aan de lijst met modi

    return sorted(modi)  # Geef de gesorteerde lijst met modi terug
