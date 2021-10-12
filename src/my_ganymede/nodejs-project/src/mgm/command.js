/*
 * Module that contains the class for a command.
 */

'use strict';

// Available types
let types = ['callback'];

class Command {
    constructor(section, description, command, type, callback) {
        // Check if the given type is correct
        if (types.indexOf(type) === -1) {
            throw `Type "${type}" is not a valid Command type"`
        }

        // Set the object variables
        this.section = section;
        this.description = description;
        this.command = command;
        this.type = type;
        this.callback = callback;
    }
}

/*
 * Export the class
 */

export default Command;
