// Store to save UI information about the dashboard
export default {
    state() {
        return {
            navigation_visible: true,
            device_type: 'pc'
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
        }
    }
};