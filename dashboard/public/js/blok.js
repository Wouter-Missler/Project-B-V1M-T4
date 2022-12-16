class Blok {
    constructor(type, askForInputVariables = true, inputVariables = []) {
        this.type = type;
        this.inputVariables = [];
        this.displayVariables = [];
        this.tableLimit = this.type.tableLimit;
        this.tablePage = 0;

        // voeg het blok toe aan de pagina
        this.element = document.createElement('div');
        this.element.classList.add('blok');
        this.element.classList.add('loading');
        this.element.classList.add(this.type.name);
        document.querySelector('.blokken').appendChild(this.element);

        // vraag de gebruiker om de input variables
        if (askForInputVariables) {
            for (const inputVariable in this.type.inputVariables) {

                let val = prompt("voer hier uw " + this.type.inputVariables[inputVariable] + " in");
                // laat de gebruiker een waarde invoeren voor de input variable
                if (val == null || val == "") {
                    alert("Geen geldige " + this.type.inputVariables[inputVariable] + " ingevoerd! \n\n Probeer het opnieuw.");
                    this.remove();
                    return;
                }

                // sla de waarde op in de inputVariables array
                this.inputVariables.push({
                    name: inputVariable,
                    value: val
                });

            }
        } else {
            this.inputVariables = inputVariables;
        }

        let urlAddition = "";
        // voeg alle input variables toe aan de url
        for (const inputVariable in this.inputVariables) {
            let firstItem = this.inputVariables.indexOf(this.inputVariables[inputVariable]) == 0;
            urlAddition += (!firstItem ? "&" : "?") + this.inputVariables[inputVariable].name + "=" + this.inputVariables[inputVariable].value;
        }

        // haal de display variables op
        loadDataFromUrl(apiURL + "/api/" + this.type.apiType.toLowerCase() + urlAddition).then(data => {
            if (data == "no-data") {
                // als de data niet opgehaald kon worden, geef een error en stop de functie
                alert("Er is iets fout gegaan bij het ophalen van de data, probeer het later opnieuw. \n het kan zijn dat het profiel privé is of dat de gebruiker niet bestaat.");
                this.remove();
                return;
            }

            // ga door alle display variables heen, en sla de overeenkomende data uit de api op in de displayVariables array
            if (!this.type.dataIsArray) {
                for (const displayVariable in this.type.displayVariables) {
                    this.displayVariables.push({
                        type: this.type.displayVariables[displayVariable],
                        name: this.type.displayVariableNames[displayVariable],
                        value: data[displayVariable]
                    });
                }
            }

            if (this.type.dataIsArray) {
                let dataArray = data;
                for (const location of this.type.arrayLocation) {
                    dataArray = dataArray[location];
                }

                // ga door dataArray heen
                for (const d of dataArray) {
                    for (const displayVariable in this.type.displayVariables) {
                        this.displayVariables.push({
                            type: this.type.displayVariables[displayVariable],
                            name: this.type.displayVariableNames[displayVariable],
                            value: d[displayVariable]
                        });
                    }
                }
            }

            // voeg elementen toe aan het blok
            this.title = document.createElement('h2');
            this.title.innerHTML = this.type.name + " van <span class='titleName'>laden...</span>";

            // voeg een knop toe om het blok te verwijderen
            this.removeButton = document.createElement('button');
            this.removeButton.innerHTML = "<img src='./assets/x-icon.svg' alt='remove'>";
            this.removeButton.classList.add('removeButton');
            this.removeButton.addEventListener('click', () => {
                this.remove();
                // sla blokken op
                saveBlocks();
            });
            this.title.appendChild(this.removeButton);

            this.update();
        });
    }

    createElement(t, data = null, addTo) {
        // check voor ! in de t string, 
        // haal deze en alles erna eruit en sla de waarde op in de special variabele
        let special = t.includes("!") ? t.split("!")[1] : null;
        let type = t.includes("!") ? t.split("!")[0] : t;
        let toAppend;

        // voeg de benodigde elementen toe aan het blok, afhankelijk van het type
        if (type == "table") {
            // maak een tabel aan
            this.table = document.createElement('table');
            toAppend = this.table;

            // voeg de header toe
            this.tableHeader = document.createElement('thead');
            this.table.appendChild(this.tableHeader);

            // voeg de header rij toe
            let row = document.createElement('tr');
            this.tableHeader.appendChild(row);

            // voeg de header kolommen toe
            let column = document.createElement('th');
            column.innerHTML = "Naam";
            row.appendChild(column);

            let column2 = document.createElement('th');
            column2.innerHTML = "Waarde";
            row.appendChild(column2);

            // voeg de body toe
            this.tableBody = document.createElement('tbody');
            this.table.appendChild(this.tableBody);

            // voeg de rijen toe gebaseerd op de displayVariables lijst
            for (let i = 0; i < Math.min(this.displayVariables.length, this.tableLimit); i++) {
                // haal current op, met de goeie pagina 
                let currentIndex = i + this.tablePage * this.tableLimit;
                if (currentIndex >= this.displayVariables.length) {
                    break; // als de currentIndex groter is dan de lengte van de lijst, stop dan
                }
                let current = this.displayVariables[currentIndex];

                // voeg de rij toe
                let row = document.createElement('tr');
                this.tableBody.appendChild(row);

                // voeg de kolom toe
                let column = document.createElement('td');
                column.innerHTML = current.name;
                row.appendChild(column);

                // voeg de kolom toe
                let column2 = document.createElement('td');
                this.createElement(current.type, current.value, column2);
                row.appendChild(column2);
            }
        }

        if (type == "p") {
            // maak een p element aan
            let p = document.createElement('p');
            p.innerHTML = data;
            toAppend = p
        }

        if (type == "img") {
            // maak een img element aan
            let img = document.createElement('img');
            img.src = data;
            toAppend = img
        }

        if (type == "a") {
            // maak een a element aan
            let a = document.createElement('a');
            a.href = data; // data is hier de url
            a.innerHTML = "Klik hier"; // standaard tekst
            a.target = "_blank"; // open in nieuw tabblad
            toAppend = a;
        }

        if (type == "tableNav") {
            // voeg de knoppen toe
            let container = document.createElement('div');
            container.classList.add('tableButtons');
            toAppend = container;

            // voeg de knoppen toe
            let prevButton = document.createElement('button');
            prevButton.innerHTML = "<img src='./assets/arrow-left.svg' alt='vorige'>";
            prevButton.classList.add('prevButton');
            prevButton.addEventListener('click', () => {
                this.changePage(this.tablePage - 1);
            });
            container.appendChild(prevButton);

            let pageText = document.createElement('span');
            pageText.innerHTML = "Pagina " + (this.tablePage + 1) + " van " + Math.ceil(this.displayVariables.length / this.tableLimit);
            container.appendChild(pageText);

            let nextButton = document.createElement('button');
            nextButton.innerHTML = "<img src='./assets/arrow-right.svg' alt='volgende'>";
            nextButton.classList.add('nextButton');
            nextButton.addEventListener('click', () => {
                this.changePage(this.tablePage + 1);
            });
            container.appendChild(nextButton);
        }

        // als we nog iets speciaals moeten doen, doen we dat hier
        if (special == "unix") {
            // zet de unix timestamp om naar een datum
            toAppend.innerHTML = new Date(toAppend.innerHTML * 1000).toLocaleDateString();
        }

        if (special == "min") {
            // zet de minuten om naar een leesbare waarde
            let hours = Math.floor(toAppend.innerHTML / 60);
            let minutes = toAppend.innerHTML % 60;
            toAppend.innerHTML = hours + " uur en " + minutes + " minuten";
        }

        if (special == "status") {
            // zet de status om naar een leesbare waarde
            let values = ["Offline", "Online", "Busy", "Away", "Snooze", "Looking to trade", "Looking to play"];
            toAppend.innerHTML = values[toAppend.innerHTML];
        }

        if (special == "steamidToName") {
            // zet de steam id om naar een naam
            this.steamidToName(toAppend.innerHTML, toAppend);
        }

        addTo.appendChild(toAppend);
    }

    async steamidToName(steamid, element = null) {
        // als de naam al bekend is, geef deze terug
        if (steamidToNameCache[steamid]) {
            if (element) {
                element.innerHTML = steamidToNameCache[steamid];
            }
            return steamidToNameCache[steamid];
        }

        // als de naam nog niet bekend is, vraag deze op
        let name = await loadDataFromUrl(apiURL + "/api/getplayersummaries?steamID=" + steamid + "&variable=personaname", false);

        // sla de naam op in de cache
        steamidToNameCache[steamid] = name;

        // als er een element is meegegeven, zet de naam erin
        if (element) {
            element.innerHTML = name;
        }

        // geef de naam terug
        return name;
    }

    update() {
        // maak het blok leeg
        this.element.innerHTML = "";

        // voeg de loading class toe aan het blok
        this.element.classList.add('loading');

        this.steamidToName(this.inputVariables[0].value, this.title.querySelector('.titleName')).then(() => {
            if (this.type.dataIsArray) {
                let amount = this.displayVariables.length / Object.keys(this.type.displayVariables).length;
                this.title.querySelector('.titleName').innerHTML += " (" + amount + ")";
            }
        });
        this.element.appendChild(this.title);

        this.createElement(this.type.displayType, null, this.element);

        // als er een tabel is, en er meer dan 1 pagina is, voeg dan de navigatie toe
        if (this.type.displayType == "table" && Math.ceil(this.displayVariables.length / this.tableLimit) > 1) {
            this.createElement("tableNav", null, this.element);
        }

        // haal de loading class van het blok
        this.element.classList.remove('loading');
    }

    changePage(page) {
        // als de pagina niet veranderd, doe dan niks
        if (this.tablePage == page) {
            return;
        }

        // als de pagina wel veranderd, verander de pagina
        this.tablePage = page;

        // check of de pagina niet te hoog / laag is
        if (this.tablePage < 0) {
            this.tablePage = 0;
        }
        if (this.tablePage > Math.ceil(this.displayVariables.length / this.tableLimit) - 1) {
            this.tablePage = Math.ceil(this.displayVariables.length / this.tableLimit) - 1;
        }

        // update het blok
        this.update();
    }
    remove() {
        // haal het blok uit de huidigeBlocks array
        huidigeBlocks.splice(huidigeBlocks.indexOf(this), 1);
        // verwijder het blok uit de pagina
        this.element.remove();
    }
}