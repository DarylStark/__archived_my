/*
 * Module that contains the main class for the My Ganymede frontend
 */

'use strict';

import UI from './ui.js';
import Commands from './commands.js'

class Ganymede {
    constructor() {
        // Initialize the modules of the application.
        this.ui = new UI();
        this.commands = new Commands();
    }
}

/*
 * Initiate a instance of the class and export it, so it can be used by
 * UI apps and components.
 */

export default new Ganymede();
