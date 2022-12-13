from flask import Flask  # importeer de Flask class
from flask_cors import CORS

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
