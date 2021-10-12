/*
 * Module that contains the main class for the My Ganymede frontend
 */


import UI from './ui.js';

class Ganymede {
    constructor() {
        // Initialize the modules of the application.
        console.log('UI is started');
        this.ui = new UI();
    }
}

/*
 * Initiate a instance of the class and export it, so it can be used by
 * UI apps and components.
 */

export default new Ganymede();
