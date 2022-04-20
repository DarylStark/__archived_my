// Import the 'createStore' method from Veux
import { createRouter, createWebHistory } from 'vue-router'

// Import the pages
import Dashboard from './pages/Dashboard'
import Tags from './pages/Tags'
import Notes from './pages/Notes'

// Create a store for central state management
export default createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes: [
        {
            path: '/dashboard',
            component: Dashboard
        },
        {
            path: '/tags',
            component: Tags
        },
        {
            path: '/notes',
            component: Notes
        },
    ]
});
