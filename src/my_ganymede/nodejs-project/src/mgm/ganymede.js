/*
 * Module that contains the main class for the My Ganymede frontend
 */

'use strict';

import UI from './ui.js';
import Commands from './commands.js'
import Command from './command.js';
import API from './api.js';
import APICommand from './api_command.js';

class Ganymede {
    constructor() {
        // Initialize the modules of the application.
        this.ui = new UI();
        this.commands = new Commands();
        this.api = new API();
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

        // Commands for 'dashboard'
        if (app === 'dashboard') {
            this.commands.register(new Command('User session', 'logout', 'userssion.logout', 'callback', () => {
                // Send the command to logout the user
                this.api.execute(
                    new APICommand(
                        'aaa',
                        'logout',
                        'GET',
                        null,
                        function () {
                            // Logged out; redirect the user to the
                            // login screen
                            window.location.href = '/ui/login';
                        },
                        function () {
                            // TODO: Give an error
                            console.log('Error while logging out');
                        }
                    )
                );
            }));
        }
    }
}

/*
 * Initiate a instance of the class and export it, so it can be used by
 * UI apps and components.
 */

export default new Ganymede();
