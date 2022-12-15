class Blok {
    constructor(type) {
        this.type = type;
        this.inputVariables = [];

        for (let i = 0; i < this.type.inputVariables.length; i++) {
            let inputVariable = this.type.inputVariables[i];
            this.inputVariables.push({
                name: inputVariable.keys()[0],
                value: prompt("voer hier uw " + inputVariable.values()[0] + " in")
            });
        }

        // add block html to the page
        this.element = document.createElement('div');
        this.element.classList.add('blok');
        this.element.classList.add(this.type.name);
        document.querySelector('.blokken').appendChild(this.element);

        console.log(this)
    }

    update() {
        // update the block
    }
}