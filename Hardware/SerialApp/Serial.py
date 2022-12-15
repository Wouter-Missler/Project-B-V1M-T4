import requests
from serial.tools import list_ports
import serial

key = "EB385AB42E26CF8504625DB7C66DC187"
accstatlink = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={}&format=json&steamids=STEAMID".format(key)
steamid = "765261198086298135"

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
    line = port.read(1000)
    print(line.decode())
    return line.decode()

serialports = list_ports.comports()

for i, port in enumerate(serialports):
    print(str(i) + ". " + str(port.device))

picoportkeuze = int(input("Met welke poort is je pico verbonden?"))
picoport = serialports[picoportkeuze].device

print(picoport)

with serial.Serial(port=picoport, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serialport:
    if serialport.isOpen():
        print("Serial port: ", serialport.name)
    else:
        print("Serial port ", serialport.name, " openen")
        serialport.open()

    try:
        while True:
            keuze = input("Maak een keuze(aan of uit): ")
            if keuze == "aan":
                data = "1\r"
                serialport.write(data.encode())
            elif keuze == "uit":
                data = "0\rSeria"
                serialport.write(data.encode())

    except KeyboardInterrupt:
        print("Afsluiten")
    finally:
        serialport.close()
        print("Serial port gesloten, dag!")
