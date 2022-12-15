class Blok {
    constructor(type) {
        this.type = type;

        // add block html to the page
        this.element = document.createElement('div');
        this.element.classList.add('blok');
        this.element.classList.add(this.type);
        document.querySelector('.blokken').appendChild(this.element);
    }

    init() {
        // init the block
        if (this.type === 'user') {
            // display data from a user
        }
    }

    update() {
        // update the block
    }
}