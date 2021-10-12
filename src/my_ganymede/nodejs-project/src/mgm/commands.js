/*
 * Module that contains the class for commands.
 */

'use strict';

import Command from './command.js'

class Commands {
    constructor() {
        // Set a empty object for commands
        this.commands = new Object();
    }

    register(command) {
        // Method to register a command
        if (Object.getPrototypeOf(command) === Command.prototype) {
            // Register the command
            this.commands[command.command] = command;

            // Done
            return;
        }

        // Command not of the correct type
        throw `Command "${command}" is not a valid Command-object`;
    }

    execute(command) {
        // Method to execute a command
        if (command in this.commands) {
            let cmd = this.commands[command];
            if (cmd.type === 'callback') {
                // Execute the callback method
                cmd.callback();
            }

            // Done!
            return;
        }

        // Command not found
        throw `Command "${command}" not found`;
    }
}

/*
 * Initiate a instance of the class and export it, so it can be used by
 * UI apps and components.
 */

export default Commands;
