class Blok {
    constructor(type, askForInputVariables = true, inputVariables = []) {
        this.type = type;
        this.inputVariables = [];
        this.displayVariables = [];
        this.dataLimit = this.type.dataLimit;
        this.dataPage = 0;
        this.dataArrayLength = this.dataLimit;

        // voeg het blok toe aan de pagina
        this.element = document.createElement('div');
        this.element.classList.add('blok');
        this.element.classList.add('loading');
        this.element.classList.add(this.type.name);
        document.querySelector('.blokken').appendChild(this.element);

        // vraag de gebruiker om de input variables
        if (askForInputVariables) {
            for (const inputVariable in this.type.inputVariables) {
                let inputVar = {
                    name: null,
                    value: null
                }

                if (this.type.inputVariables[inputVariable].includes("!")) {
                    // check of de input varaible een ! heeft, zo ja, doe iets speciaals gebaseerd op wat na de ! staat

                    let specialInputVariable = this.type.inputVariables[inputVariable].split("!")[1];

                    if (specialInputVariable.includes("limit")) {
                        // split de string op de : en sla de tweede waarde op in de amount variabele
                        let amount = specialInputVariable.split(":")[1];

                        inputVar.name = inputVariable;
                        inputVar.value = amount;
                    }

                    if (specialInputVariable == "offset") {
                        inputVar.name = inputVariable;
                        inputVar.value = this.dataPage * this.dataLimit;
                    }
                } else {
                    // anders, vraag de gebruiker om de input variable

                    let val = prompt("voer hier uw " + this.type.inputVariables[inputVariable] + " in");
                    // laat de gebruiker een waarde invoeren voor de input variable
                    if (val == null || val == "") {
                        alert("Geen geldige " + this.type.inputVariables[inputVariable] + " ingevoerd! \n\n Probeer het opnieuw.");
                        this.remove();
                        return;
                    }

                    inputVar = {
                        name: inputVariable,
                        value: val
                    }

                }

                // sla de waarde op in de inputVariables array
                this.inputVariables.push(inputVar);

            }
        } else {
            this.inputVariables = inputVariables;
        }

        this.getDisplayVariables();

        // voeg dit blok toe aan de huidige blokken
        huidigeBlocks.push(this);
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
            for (let i = 0; i < Math.min(this.displayVariables.length, this.dataLimit); i++) {
                // haal current op, met de goeie pagina 
                let currentIndex = i + this.dataPage * this.dataLimit;
                if (this.dataArrayLength !== this.dataLimit) currentIndex = i;
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
                this.changePage(this.dataPage - 1);
            });
            container.appendChild(prevButton);

            let pageText = document.createElement('span');
            pageText.innerHTML = "Pagina " + (this.dataPage + 1) + " van " + Math.ceil(this.displayVariables.length / this.dataArrayLength);
            container.appendChild(pageText);

            let nextButton = document.createElement('button');
            nextButton.innerHTML = "<img src='./assets/arrow-right.svg' alt='volgende'>";
            nextButton.classList.add('nextButton');
            nextButton.addEventListener('click', () => {
                this.changePage(this.dataPage + 1);
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

    getDisplayVariables(doUpdate = true) {
        this.displayVariables = [];

        // check of we inputvariables moeten updaten, voor nu alleen bij de naam offset
        // ga door alle input variables heen
        for (const inputVariable in this.inputVariables) {
            // als de input variable een offset is
            if (this.inputVariables[inputVariable].name == "offset") {
                // zet de offset op de pagina die we nu aan het bekijken zijn
                this.inputVariables[inputVariable].value = this.dataPage;
            }
        }

        let urlAddition = "";
        // voeg alle input variables toe aan de url
        for (const inputVariable in this.inputVariables) {
            let firstItem = this.inputVariables.indexOf(this.inputVariables[inputVariable]) == 0;
            urlAddition += (!firstItem ? "&" : "?") + this.inputVariables[inputVariable].name + "=" + this.inputVariables[inputVariable].value;
        }

        console.log(apiURL + "/api/" + this.type.apiType.toLowerCase() + urlAddition);

        // haal de display variables op
        loadDataFromUrl(apiURL + "/api/" + this.type.apiType.toLowerCase() + urlAddition).then(data => {
            if (data == "no-data") {
                // als de data niet opgehaald kon worden, geef een error en stop de functie
                alert("Er is iets fout gegaan bij het ophalen van de data, probeer het later opnieuw. \n het kan zijn dat het profiel privé is of dat de gebruiker niet bestaat.");
                this.remove();
                return;
            }

            // als de data een gelimiteerd aantal items heeft, sla de originele lengte op voor de paginering
            if (data.originalLength) {
                this.dataArrayLength = parseInt(data.originalLength);
                console.log(this.dataArrayLength)
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

            // als er een update nodig is, update het blok
            if (doUpdate) {
                this.update();
            }
        });
    }

    update() {
        // maak het blok leeg
        this.element.innerHTML = "";

        // voeg de loading class toe aan het blok
        this.element.classList.add('loading');

        // voeg elementen toe aan het blok
        this.title = document.createElement('h2');
        this.title.innerHTML = this.type.name + " van <span class='titleName'>laden...</span>";

        // pas de titel aan als er een naam moet worden weergegeven
        if (this.type.showFromInTitle) {
            this.steamidToName(this.inputVariables[0].value, this.title.querySelector('.titleName')).then(() => {
                if (this.type.dataIsArray) {
                    let amount = this.displayVariables.length / Object.keys(this.type.displayVariables).length;
                    this.title.querySelector('.titleName').innerHTML += " (" + amount + ")";
                }
            });
        } else {
            this.title.innerHTML = this.type.name;
        }

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

        this.element.appendChild(this.title);

        this.createElement(this.type.displayType, null, this.element);

        // als er een tabel is, en er meer dan 1 pagina is, voeg dan de navigatie toe
        if (this.type.displayType == "table" && Math.ceil(this.displayVariables.length / this.dataLimit) > 1) {
            this.createElement("tableNav", null, this.element);
        }

        // haal de loading class van het blok
        this.element.classList.remove('loading');
    }

    changePage(page) {
        // als de pagina niet veranderd, doe dan niks
        if (this.dataPage == page) {
            return;
        }

        // als de pagina wel veranderd, verander de pagina
        this.dataPage = page;

        // check of de pagina niet te hoog / laag is
        if (this.dataPage < 0) {
            this.dataPage = 0;
        }

        if (this.dataArrayLength == this.dataLimit) {
            if (this.dataPage > Math.ceil(this.displayVariables.length / this.dataLimit) - 1) {
                this.dataPage = Math.ceil(this.displayVariables.length / this.dataLimit) - 1;
            }

            // update het blok
            this.update();
        } else {
            // gebruik de originele lengte van de data array om te checken of de pagina niet te hoog is
            if (this.dataPage > Math.ceil(this.dataArrayLength / this.dataLimit) - 1) {
                this.dataPage = Math.ceil(this.dataArrayLength / this.dataLimit) - 1;
            }
            // update de display variables
            this.getDisplayVariables();
        }
    }
    remove() {
        // haal het blok uit de huidigeBlocks array
        huidigeBlocks.splice(huidigeBlocks.indexOf(this), 1);
        // verwijder het blok uit de pagina
        this.element.remove();
    }
}