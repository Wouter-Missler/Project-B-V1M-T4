let currentUser; // houd de huidige gebruiker bij
let blockTypes; // houd de block types bij
let huidigeBlocks = []; // houd de huidige blocks bij
let apiURL = "https://woutm.eu.pythonanywhere.com"; // houd de api url bij
if (location.hostname === "localhost" || location.hostname === "127.0.0.1")
    apiURL = "http://localhost:5000"; // voor local testing

let steamidToNameCache = []; // houd een cache bij van steamid naar naam

window.onload = function () {
    // haal de block types op
    loadDataFromUrl(apiURL + "/blocktypes").then(data => {
        blockTypes = data; // sla de json data op in de blockTypes variabele

        // voeg knoppen toe voor alle block types
        for (const blockType in blockTypes) {
            let button = document.createElement("button");
            button.innerHTML = blockTypes[blockType].name;
            button.addEventListener("click", function () {
                // voeg een blok toe met de gekozen block type
                createBlock(blockTypes[blockType]);
            });
            document.querySelector(".block-add .block-add-popup").appendChild(button);
        }

        // console.log("blocktypes: ", blockTypes)
    }).then(() => {

        // check of er een steamID in de localstorage staat
        if (localStorage.getItem("steamID") !== null) {
            // haal de steamID op uit de localstorage
            let steamID = localStorage.getItem("steamID");

            // zet de steamID in de user popup id
            document.getElementById("userPopupID").innerHTML = steamID;

            // update de gebruikers data
            updateUser()
        } else {
            // zet de steamID in de user popup id
            document.getElementById("userPopupID").innerHTML = "Niet ingelogd";
        }

    });
}

// voeg een event listener toe aan de user avatar om de user popup te tonen of te verbergen
document.querySelector(".user-avatar").addEventListener("click", function () {
    document.querySelector(".user-popup").classList.toggle("hidden"); // toggle de user popup
});

// voeg een event listener toe aan de add block knop om een blok toe te voegen
document.querySelector(".block-add button").addEventListener("click", function () {
    // check of de gebruiker is ingelogd
    if (localStorage.getItem("steamID") === '') {
        alert("Je moet ingelogd zijn om blokken toe te voegen!");
        return;
    }

    document.querySelector(".block-add-popup").classList.toggle("hidden"); // toggle de user popup
});

// algemeen functie om json data op te halen van een url
async function loadDataFromUrl(url, useJson = true) {
    const response = await fetch(url); // wacht tot de data binnen is
    var data = await response.text(); // zet de data om naar text

    if (useJson && data !== "no-data") {
        data = JSON.parse(data); // zet de data om naar json
    }

    return data; // return de data
}

async function saveDataToUrl(url, data) {
    // save de doorgegeven data naar de doorgegeven url, zonder de pagina te herladen
    await fetch(url, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        },
    })
}

// functie om de gebruikers data te updaten
function updateUser() {
    let steamID = localStorage.getItem("steamID"); // haal de steamID op uit de localstorage

    if (steamID) {
        // haal de opgeslagen blokken op
        getSavedBlocks(steamID);

        loadDataFromUrl(apiURL + "/api/getplayersummaries?steamID=" + steamID).then(data => {
            currentUser = data; // sla de json data op in de currentUser variabele

            if (currentUser == "no-data") {
                alert("Gebruiker is een prive profiel of bestaat niet, je wordt als gast ingelogd.");
                currentUser = {
                    avatar: "./assets/avatar-placeholder.jpg",
                    personaname: "Gast",
                    steamid: steamID
                }
            }

            document.querySelector(".user-avatar img").src = currentUser.avatar; // zet de avatar
            document.querySelector(".user-popup .username").innerHTML = "Huidige gebruiker: " + currentUser.personaname; // zet de gebruikersnaam
            document.querySelector(".user-popup .user-id .id").innerHTML = currentUser.steamid; // zet de steamID	
        });
    } else {
        // haal de opgeslagen blokken op
        getSavedBlocks();

        currentUser = null; // zet de currentUser variabele op null
        document.querySelector(".user-avatar img").src = "./assets/avatar-placeholder.jpg"; // zet de avatar terug naar de placeholder
        document.querySelector(".user-popup .username").innerHTML = "Huidige gebruiker: Niet ingelogd"; // zet de gebruikersnaam
        document.querySelector(".user-popup .user-id .id").innerHTML = "Niet ingelogd"; // zet de steamID
    }
}

function changeUser() {
    let steamID = prompt("SteamID:"); // vraag de gebruiker om een steamID

    if (steamID !== "" && steamID !== null && steamID.match(/^[0-9]+$/) || steamID.length !== 17) { // check of de steamID niet leeg of null is en of het een geldige steamID is
        // sla de steamID op in de localstorage
        localStorage.setItem("steamID", steamID);
    } else {
        // verwijder de steamID uit de localstorage
        localStorage.removeItem("steamID");
    }

    // update de gebruikers data
    updateUser();
}

function getSavedBlocks(steamID) {
    huidigeBlocks = []; // maak de huidigeBlocks array leeg
    document.querySelector(".blokken").innerHTML = ""; // maak het element .blokken leeg

    if (steamID === undefined) return; // check of de steamID is meegegeven, zo niet, stop de functie

    // haal de opgeslagen blokken op en voeg ze toe aan de huidigeBlocks array
    loadDataFromUrl(apiURL + "/api/blocksaved?steamID=" + steamID).then(data => {
        let savedBlocks = data.blocks; // sla de json data op in de savedBlocks variabele

        // loop door alle opgeslagen blokken
        savedBlocks.forEach(blok => {
            // voeg de block toe aan de huidigeBlocks array
            new Blok(blockTypes.find(b => b.name == blok.name), false, blok.inputVariables);
        });
    });
}

function saveBlocks() {
    let steamID = localStorage.getItem("steamID"); // haal de steamID op uit de localstorage

    // check of de gebruiker is ingelogd
    if (steamID == null) {
        alert("Je moet ingelogd zijn om blokken op te slaan!");
        return;
    }

    // maak een array aan met de opgeslagen blokken
    let savedBlocks = [];

    // loop door alle huidige blocks
    huidigeBlocks.forEach(blok => {
        // voeg de block toe aan de savedBlocks array
        savedBlocks.push({
            name: blok.type.name,
            inputVariables: blok.inputVariables
        })
    });

    let data = {
        steamID: steamID,
        blocks: savedBlocks
    }

    // sla de blokken op zonder de pagina te herladen
    saveDataToUrl(apiURL + "/api/blocksave", data);
}

function createBlock(type) {
    // maak een nieuwe block aan, deze wordt via de constructor toegevoegd aan de huidigeBlocks array
    let blok = new Blok(type);
}