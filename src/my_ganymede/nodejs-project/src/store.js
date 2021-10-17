// Import the 'createStore' method from Veux
import { createStore } from 'vuex'

// Create a store for central state management
export default createStore({
    state() {
        return {
            navigation_visible: true,
            user_fullname: '<user fullname>' // TODO: has to be filled with real users fullname
        }
    },
    mutations: {
        navigation_visible_toggle(state) {
            state.navigation_visible = !state.navigation_visible;
        }
    }
});
