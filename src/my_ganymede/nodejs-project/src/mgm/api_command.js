/*
 * Module that contains the class that defines API commands.
 */

'use strict';

// Available types
let methods = ['GET', 'POST'];

class APICommand {
    constructor(group, endpoint, method = 'GET', data, cb_success, cb_catch) {
        // Check if the given method is correct
        if (methods.indexOf(method) === -1) {
            throw `Method "${method}" is not a valid HTTP method"`
        }

        this.group = group;
        this.endpoint = endpoint;
        this.method = method;
        this.cb_success = cb_success;
        this.cb_catch = cb_catch;
        this.data = data;
    }
}

/*
 * Export the class
 */

export default APICommand;
