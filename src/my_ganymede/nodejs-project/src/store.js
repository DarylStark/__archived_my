// Import the 'createStore' method from Veux
import { createStore } from 'vuex'

import ui from './store/ui';
import user_session from './store/user_session';

// Create a store for central state management
export default createStore({
    modules: {
        ui: ui,
        user_session: user_session
    },
});
