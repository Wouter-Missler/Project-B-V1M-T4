class Blok {
    constructor(type, askForInputVariables = true, inputVariables = []) {
        this.type = type;
        this.inputVariables = [];
        this.displayVariables = [];

        // vraag de gebruiker om de input variables
        if (askForInputVariables) {
            for (const inputVariable in this.type.inputVariables) {

                let val = prompt("voer hier uw " + this.type.inputVariables[inputVariable] + " in");
                // laat de gebruiker een waarde invoeren voor de input variable
                if (val == null || val == "") {
                    alert("Geen geldige " + this.type.inputVariables[inputVariable] + " ingevoerd! \n\n Probeer het opnieuw.");
                    val = prompt("voer hier uw " + this.type.inputVariables[inputVariable] + " in");
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
        loadDataFromUrl("https://woutm.eu.pythonanywhere.com/api/" + this.type.apiType.toLowerCase() + urlAddition).then(data => {
            // ga door alle display variables heen, en sla de overeenkomende data uit de api op in de displayVariables array
            console.log(data)

            for (const displayVariable in this.type.displayVariables) {
                this.displayVariables.push({
                    type: this.type.displayVariables[displayVariable],
                    name: this.type.displayVariableNames[displayVariable],
                    value: data[displayVariable]
                });
            }

            // voeg het blok toe aan dashboard
            this.element = document.createElement('div');
            this.element.classList.add('blok');
            this.element.classList.add(this.type.name);
            let title = document.createElement('h2');
            title.innerHTML = this.type.name;
            this.element.appendChild(title);
            document.querySelector('.blokken').appendChild(this.element);

            console.log(this)

            this.createElement(this.type.displayType, null, this.element);
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
            for (const displayVariable in this.displayVariables) {
                let current = this.displayVariables[displayVariable];

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

        // als we nog iets speciaals moeten doen, doen we dat hier
        if (special == "unix") {
            // zet de unix timestamp om naar een datum
            toAppend.innerHTML = new Date(toAppend.innerHTML * 1000).toLocaleDateString();
        }

        if (special == "status") {
            // zet de status om naar een leesbare waarde
            let values = ["Offline", "Online", "Busy", "Away", "Snooze", "Looking to trade", "Looking to play"];
            toAppend.innerHTML = values[toAppend.innerHTML];
        }

        addTo.appendChild(toAppend);
    }

    update() {
        // update the block
    }
}