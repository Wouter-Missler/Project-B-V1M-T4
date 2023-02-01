# Project STEAM
Periode B

Gemaakt door: Mark, Wouter en Annabel

De **hoofdopdracht luid**: "Maak een grafische weergave die inzicht geeft in het gaming gedrag van jouw vrienden op het platform Steam, ondersteund door één of meer hardwarecomponenten."

Afbeelding van oplossing:
![alt text](https://canvas.hu.nl/courses/32737/files/3080994/preview "image Title")

Het project is opgebouwd uit:
 1. Een dashboard
 2. Een database
 3. Stuk hardware 
 4. BIM onderdelen

 # Gebruikte Libraries
 1. [flask python](https://flask.palletsprojects.com/en/2.2.x/)\
wordt gebruikt om via het dashboard de back-end te benaderen, via een web URL.\
Om de webserver te starten, gebruik je het commando: ``flask (bestandnaam zonder .py) run``\
Daarna is de webserver te bereiken via: ``localhost:5000/functienaam``
 2. [flask-cors](https://flask-cors.readthedocs.io/en/latest/)\
wordt gebruikt om de webserver te laten communiceren met de database. Door de CORS (Cross-Origin Resource Sharing) te activeren, kan de webserver de database benaderen.
Deze library wordt gebruikt door de command ``CORS(app)`` in de app.py te zetten. Hierdoor worden de CORS headers aangepast en kan de webserver de database benaderen.
3. [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html)\
wordt gebruikt om de database te benaderen. De database is een MySQL database. De library wordt gebruikt door de command ``import mysql.connector`` in de app.py te zetten. Hierdoor kan de webserver de database benaderen.
4. [json] (https://docs.python.org/3/library/json.html)\
wordt gebruikt om data om te zetten naar JSON. De library wordt gebruikt door de command ``import json`` in de app.py te zetten. Hierdoor kan de webserver de data omzetten naar JSON.
5. [requests] (https://docs.python-requests.org/en/master/)\
wordt gebruikt om data van de steam API te halen. De library wordt gebruikt door de command ``import requests`` in de app.py te zetten. Hierdoor kan de webserver de data van de API halen.

# Lokale installatie
Om het dashboard lokaal te runnen moet je de volgende stappen doorlopen:
1. Clone de repository
2. installeer de volgende libraries: flask, flask-cors, mysql-connector-python, json, requests, dit kan door de commando's ``pip install flask``, ``pip install flask-cors``, ``pip install mysql-connector-python``, ``pip install json``, ``pip install requests`` te gebruiken.
3. start de webserver door het commando ``flask app.py run`` te gebruiken in de terminal.
4. gebruik een python webserver om de index.html te runnen. Dit kan door het commando ``python -m http.server`` te gebruiken in de terminal. Hiervoor moet je wel eerst in de terminal navigeren naar de map waar de index.html staat. Dit is vanuit de root dit pad: 'dashboard/public'.
