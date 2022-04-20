// Import the 'createStore' method from Veux
import { createRouter, createWebHistory } from 'vue-router'

// Import the pages
import Dashboard from './pages/Dashboard'
import Tags from './pages/Tags'
import Notes from './pages/Notes'

// Error page
import Error404 from './pages/errors/Error-404'

// Create a store for central state management
export default createRouter({
    history: createWebHistory('/ui/'),
    routes: [
        {
            // The homepage is a redirect to the dashboard
            path: '/',
            redirect: '/dashboard',
        },
        {
            path: '/dashboard',
            name: 'dashboard',
            component: Dashboard
        },
        {
            path: '/tags',
            name: 'tags',
            component: Tags
        },
        {
            path: '/notes',
            name: 'notes',
            component: Notes
        },
        {
            // Error page
            path: '/:pathMatch(.+)',
            component: Error404
        }
    ]
});
