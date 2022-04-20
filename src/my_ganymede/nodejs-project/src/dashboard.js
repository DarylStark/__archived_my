// Import Vue
import { createApp } from 'vue'

// Import the store
import store from './store'

// Import the router
import router from './router';

// Import the Ganymade code
import Ganymede from './mgm/ganymede.js'

// Import the Dashboard Application
import GanymedeDashboard from './apps/GanymedeDashboard.vue'

// Create the app
const dashboard = createApp(GanymedeDashboard)

// Register commands for the Dashboard
Ganymede.register_commands('dashboard');

// Specify the store
dashboard.use(store);

// Specify the router
dashboard.use(router);

// Mount the app
dashboard.mount('#app_dashboard')