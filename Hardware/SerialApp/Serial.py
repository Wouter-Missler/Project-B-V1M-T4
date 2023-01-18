import requests
from serial.tools import list_ports
import serial
import time
from time import sleep
import json

key = "EB385AB42E26CF8504625DB7C66DC187"
accstatlink = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={}&format=json&steamids=STEAMID".format(key)
steamid = "76561198086298135"

def getfriendids(apikey):
    """"
    Functie voor het ophalen van friendids
    ARGs:
        Apikey = de SteamAPI key
    Returns:
        list met steamid's
    """
    response = requests.get("http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={}&steamid={}&relationship=friend".format(apikey, steamid))
    resjson = response.json()
    friendlist = resjson['friendslist']
    steamids = []
    for friend in friendlist['friends']:
        steamids.append(friend['steamid'])
    return steamids

def getonlinefriends(steamids, apikey):
    """"
    Functie voor het ophalen welke vrienden online zijn
    ARGs:
        steamids = list van steamids om te checken of ze online zijn
    Returns:
        List met realnames van online vrienden
    """
    response = requests.get("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={}&format=json&steamids={}".format(apikey, steamids))
    players = response.json()
    players = players['response']['players']
    onlineplayers = []
    for player in players:
        if player['personastate'] == 1:
            onlineplayers.append(player['realname'])
    return onlineplayers

def read_serial(port):
    """"
    Lees de poort uit
    ARGs:
        port = de COMport
    Returns:
        Antwoord van de COMport
    """
    line = port.read(1000)
    print(line.decode())
    return line.decode()

def datatojson(data):
    teversturen = {
        "steamids": {
            "76561198086298135" : {
                "onlinefriends" : {
                    "aantal" : data[0]
                }
            }
        }
    }
    with open('picoData.json', 'w') as outfile:
        json.dump(teversturen, outfile)
        print('data verzonden.')
    return


serialports = list_ports.comports()  # pakt een lijst van comports

for i, port in enumerate(serialports):  # laat alle ports zien
    print(str(i) + ". " + str(port.device))

picoportkeuze = int(input("Met welke poort is je pico verbonden?"))
picoport = serialports[picoportkeuze].device

print(picoport)

with serial.Serial(port=picoport, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serialport:  # maakt verbinding met serialport als serialport
    if serialport.isOpen():  # checkt of de poort open is ander opent hij de port
        print("Serial port: ", serialport.name)
    else:
        print("Serial port ", serialport.name, " openen")
        serialport.open()
        print(len(getonlinefriends(getfriendids(key), key)))

    try:
        while True:  # verstuurd aantal online vrienden naar de pico
            friendids = getfriendids(key)
            waarvanonline = len(getonlinefriends(friendids, key))
            data = "{}\r".format(waarvanonline)
            #serialport.write(data.encode())
            datatojson([waarvanonline])
            sleep(5)
            serialport.write(data.encode())

    except KeyboardInterrupt:  # op keyboardinterrupt sluit hij de poort1
        print("Afsluiten")
    finally:
        serialport.close()
        print("Serial port gesloten, dag!")
