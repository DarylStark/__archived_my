// Import Vue
import { createApp } from 'vue'

// Import the Ganymade code
import Ganymede from './mgm/ganymede.js'

// Import the Login Application
import GanymedeLoginForm from './apps/GanymedeLoginForm.vue'

// Register commands for the Dashboard
Ganymede.register_commands('dashboard');

// Create the app
createApp(GanymedeLoginForm).mount('#app_login')
