// Import Vue
import { createApp } from 'vue'

// Import the store
import store from './store'

// Import the Dashboard Application
import GanymedeDashboard from './apps/GanymedeDashboard.vue'

// Create the app
const dashboard = createApp(GanymedeDashboard)

// Specify the store
dashboard.use(store);

// Mount the app
dashboard.mount('#app_dashboard')