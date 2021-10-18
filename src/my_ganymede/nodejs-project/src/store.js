// Import the 'createStore' method from Veux
import { createStore } from 'vuex'

// Create a store for central state management
export default createStore({
    state() {
        return {
            navigation_visible: true,
            user_fullname: null,
            session: {
                'account': {},
                'session': {}
            },
            device_type: 'pc'
        }
    },
    mutations: {
        navigation_visible_toggle(state) {
            state.navigation_visible = !state.navigation_visible;
        },
        set_session(state, session) {
            state.session.account = session.user_account;
            state.session.session = session.session;
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
});
