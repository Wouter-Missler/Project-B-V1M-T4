import requests
from serial.tools import list_ports
import serial
import time
from time import sleep
import json
import mysql.connector

key = "EB385AB42E26CF8504625DB7C66DC187"
accstatlink = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={}&format=json&steamids=STEAMID".format(key)
apilink = "http://woutm.eu.pythonanywhere.com"
# test id = "76561198086298135"
dbhostname = "WoutM.mysql.eu.pythonanywhere-services.com"


def askID():
    """"
    Functie voor het vragen naar een steamid
    """
    id = input("wat is uw steamID?: ")
    return id

def sendData(query):
    """"
    Functie voor het versturen van data naar de database
    """
    db = mysql.connector.connect(
        host="sql7.freemysqlhosting.net",
        user="sql7594625",
        passwd="KVtzBMv5fB",
        db="sql7594625"
    )
    c = db.cursor()
    c.execute(query)
    c.commit()
    c.close()
    db.close()
    print("data verzonden")

def askData(query):
    """"
    Functie voor het vragen naar data uit de database
    """
    db = mysql.connector.connect(
        host="sql7.freemysqlhosting.net",
        user="sql7594625",
        passwd="KVtzBMv5fB",
        db="sql7594625"
    )
    c = db.cursor()
    c.execute(query)
    data = c.fetchall()
    c.close()
    db.close()
    return data

def getfriendids(steamid):
    """"
    Functie voor het ophalen van friendids

    Returns:
        list met steamid's van friends
    """
    response = requests.get("{}{}{}".format(apilink, "/api/getfriendlist?steamID=", steamid))
    resjson = response.json()
    friendlist = resjson['friendslist']
    steamids = []
    for friend in friendlist['friends']:
        steamids.append(friend['steamid'])
    return steamids

def getonlinefriends(steamids):
    """"
    Functie voor het ophalen welke vrienden online zijn
    ARGs:
        steamids = list van steamids om te checken of ze online zijn
    Returns:
        List met realnames van online vrienden
    """
    response = requests.get("{}{}{}".format(apilink, "/api/onlineplayers?steamIDs=", steamids))
    players = response.json()

    return players


def checkchange(steamid):
    global waarvanonline
    kwamonline = []
    newlist = getonlinefriends(getfriendids(steamid))
    for player in newlist:
        if player not in waarvanonline:
            kwamonline.append(player)
    waarvanonline = newlist
    print(kwamonline)
    if kwamonline:
        for player in kwamonline:
            data = "{}\n is online\r".format(player)
            return data
        else:
            return False



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
    """"
    testfunctie
    """
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
steamid = askID()
friendids = getfriendids(steamid)
waarvanonline = getonlinefriends(friendids)

for i, port in enumerate(serialports):  # laat alle ports zien
    print(str(i) + ". " + str(port.device))

picoportkeuze = int(input("Met welke poort is je pico verbonden? "))
picoport = serialports[picoportkeuze].device

print(picoport)

with serial.Serial(port=picoport, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serialport:  # maakt verbinding met serialport als serialport
    if serialport.isOpen():  # checkt of de poort open is ander opent hij de port
        print("Serial port: ", serialport.name)
    else:
        print("Serial port ", serialport.name, " openen")
        serialport.open()
        print(len(getonlinefriends(getfriendids(steamid))))

    try:
        while True:  # verstuurd aantal online vrienden naar de pico
            data = "Online: {}\r".format(len(waarvanonline))
            check = checkchange(steamid)
            if check:
                data = check
            serialport.write(data.encode())
            sleep(5)
            serialport.write(data.encode())

    except KeyboardInterrupt:  # op keyboardinterrupt sluit hij de poort1
        print("Afsluiten")
    finally:
        serialport.close()
        print("Serial port gesloten, dag!")
