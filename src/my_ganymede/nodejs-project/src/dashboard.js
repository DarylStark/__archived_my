// Import Vue
import { createApp } from 'vue'
import { createStore } from 'vuex'

// Create a store for central state management
const store = createStore({
    state() {
        return {
            navigation_visible: true
        }
    },
    mutations: {
        navigation_visible_toggle(state) {
            state.navigation_visible = !state.navigation_visible;
        }
    }
});

// Import the Dashboard Application
import GanymedeDashboard from './apps/GanymedeDashboard.vue'

// Create the app
const dashboard = createApp(GanymedeDashboard)

// Specify the store
dashboard.use(store);

// Mount the app
dashboard.mount('#app_dashboard')