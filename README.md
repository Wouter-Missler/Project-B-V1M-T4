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

