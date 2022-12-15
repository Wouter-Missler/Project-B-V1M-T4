let currentUser; // houd de huidige gebruiker bij
let blockTypes; // houd de block types bij

window.onload = function () {
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

    // haal de block types op
    loadDataFromUrl("https://woutm.eu.pythonanywhere.com/blocktypes").then(data => {
        blockTypes = data; // sla de json data op in de blockTypes variabele
    });
}

// voeg een event listener toe aan de user avatar om de user popup te tonen of te verbergen
document.querySelector(".user-avatar").addEventListener("click", function () {
    document.querySelector(".user-popup").classList.toggle("hidden"); // toggle de user popup
});

// algemeen functie om json data op te halen van een url
async function loadDataFromUrl(url) {
    const response = await fetch(url); // wacht tot de data binnen is
    var data = await response.json(); // zet de data om naar json

    return data; // return de data
}

// functie om de gebruikers data te updaten
function updateUser() {
    // haal de steamID op uit de localstorage
    let steamID = localStorage.getItem("steamID");

    loadDataFromUrl("https://woutm.eu.pythonanywhere.com/api/getplayersummaries?steamID=" + steamID).then(data => {
        currentUser = data; // sla de json data op in de currentUser variabele

        document.querySelector(".user-avatar img").src = currentUser.avatar; // zet de avatar
        document.querySelector(".user-popup .username").innerHTML = "Huidige gebruiker: " + currentUser.personaname; // zet de gebruikersnaam
        document.querySelector(".user-popup .user-id .id").innerHTML = currentUser.steamid; // zet de steamID	
    });
}

function changeUser() {
    let steamID = prompt("SteamID:"); // vraag de gebruiker om een steamID

    // check de steamID voor leeg, null, iets anders dan cijfers of niet 17 karakters lang
    if (steamID == null || steamID == "" || !steamID.match(/^[0-9]+$/) || steamID.length !== 17) { // regex check voor alleen cijfers
        alert("Geen geldige SteamID ingevoerd! \n\n Probeer het opnieuw.");
        return;
    }

    // sla de steamID op in de localstorage
    localStorage.setItem("steamID", steamID);

    // update de gebruikers data
    updateUser();
}