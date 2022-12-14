import requests

key = "EB385AB42E26CF8504625DB7C66DC187"
accstatlink = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={}&format=json&steamids=STEAMID".format(key)


response = requests.get("http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={}&steamid=76561198086298135&relationship=friend".format(key))
steamid = "76561198086298135"

def getfriendids(apikey):
    """"
    Functie voor het ophalen van friendids
    ARGs:
        Apikey = de SteamAPI key
    Returns:
        list met steamid's
    """
    response = requests.get("http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={}&steamid={}&relationship=friend".format(key, steamid))
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
    response = requests.get("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={}&format=json&steamids={}".format(key, steamids))
    players = response.json()
    players = players['response']['players']
    onlineplayers = []
    for player in players:
        if player['personastate'] == 1:
            onlineplayers.append(player['realname'])
    return onlineplayers