// Store to save UI information about the dashboard
export default {
    state() {
        return {
            navigation_visible: true,
            device_type: 'pc',
            app_title: 'My',
            page_title: ''
        }
    },
    mutations: {
        navigation_visible_toggle(state) {
            state.navigation_visible = !state.navigation_visible;
        },
        set_device_type(state, device_type) {
            // Method to set the device type. Can be either on of
            // these:
            // - pc
            // - table
            // - phone
            // Should be set on start of the application and be
            // updated as soon as the screensize changes
            state.device_type = device_type;
            console.log('Updated!');
        },
        update_title(state, page_title = '') {
            // Set the page title
            state.page_title = page_title;

            // Create the title for the window
            let window_title = state.app_title;
            if (state.page_title != '') {
                window_title += ' | ' + state.page_title;
            }

            // Set the window title
            document.title = window_title;
        }
    }
};