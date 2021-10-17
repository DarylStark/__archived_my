/*
 * Module that contains the class to execute API commands.
 */

'use strict';

import axios from 'axios';
import APICommand from './api_command';

class API {
    constructor() {
        // Set up Axios
        axios.defaults.baseURL = '/data/';
    }

    execute(command) {
        // Method to execute API commands

        // Check if we got a APICommand
        if (Object.getPrototypeOf(command) === APICommand.prototype) {
            // Construct the API URL
            let url = `${command.group}/${command.endpoint}`;

            // Run the Axios command
            axios({
                method: command.method,
                url: url,
                data: command.data
            }).then((response) => {
                if (response.data.success) {
                    // Success!
                    if (command.cb_success) {
                        command.cb_success(response.data);
                    }
                } else {
                    // Not a success
                    if (command.cb_catch) {
                        command.cb_catch(response.data);
                    }
                }
            }).catch((error) => {
                // Not a success
                if (command.cb_catch) {
                    command.cb_catch(error);
                }
            });

            // Run the Axios command
            // axios
            //     .get(url, this.credentials)
            //     .then((response) => {
            //         if (response.data.success) {
            //             // Success!
            //             if (command.cb_success) {
            //                 command.cb_success(response.data);
            //             }
            //         } else {
            //             // Not a success
            //             if (command.cb_catch) {
            //                 command.cb_catch(response.data);
            //             }
            //         }
            //     })
            //     .catch((error) => {
            //         // Not a success
            //         if (command.cb_catch) {
            //             command.cb_catch(error);
            //         }
            //     });

            // Done
            return true;
        } else {
            return false;
        }
    }
}

/*
 * Export the class
 */

export default API;
