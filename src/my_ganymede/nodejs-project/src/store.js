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
            }
        }
    },
    mutations: {
        navigation_visible_toggle(state) {
            state.navigation_visible = !state.navigation_visible;
        },
        set_session(state, session) {
            state.session.account = session.user_account;
            state.session.session = session.session;
        }
    }
});
