/*
 * Module that contains the main class for the My Ganymede frontend
 */

'use strict';

import UI from './ui.js';
import Commands from './commands.js'
import Command from './command.js';

class Ganymede {
    constructor() {
        // Initialize the modules of the application.
        this.ui = new UI();
        this.commands = new Commands();
    }

    register_commands(app) {
        // Method to register commands for specific 'apps'. The 'app'
        // can be 'login' or 'dashboard'. The 'login'-app uses
        // different commands then the 'dashboard'-app.

        // Commands for 'dashboard' and 'login'
        this.commands.register(new Command('Theme', 'Next', 'theme.next', 'callback', () => {
            // Set the next theme
            this.ui.next_theme();
        }));
    }
}

/*
 * Initiate a instance of the class and export it, so it can be used by
 * UI apps and components.
 */

export default new Ganymede();
