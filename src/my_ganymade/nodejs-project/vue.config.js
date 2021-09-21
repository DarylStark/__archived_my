module.exports = {
    devServer: {
        proxy: {
            '^/data': {
                target: 'http://localhost:3080',
                changeOrigin: true
            },
        }
    },
    pages: {
        dashboard: {
            entry: 'src/dashboard.js',
            template: 'public/dashboard.html',
            filename: 'dashboard.html',
            title: 'Dashboard'
        },
        login: {
            entry: 'src/login.js',
            template: 'public/login.html',
            filename: 'login.html',
            title: 'Login'
        }
    }
}