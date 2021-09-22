/*
 * Module that contains default functions for 'My Ganymade'
 */

import Cookies from 'js-cookie';

export default {
    'set_theme': (theme = 'from_cookie') => {
        // Set the possible themes
        const themes = {
            'dark': {
                'class': 'theme-dark'
            },
            'light': {
                'class': 'theme-light'
            }
        };

        // Set the default theme
        let default_theme = 'dark';

        // If the user specified that we have to retrieve the theme
        // from a cookie, we can retrieve the value now
        if (theme === 'from_cookie') {
            let cookie_theme = Cookies.get('theme');
            if (cookie_theme) {
                theme = cookie_theme;
            }
        }

        // If the user gave an undefined theme, or gave the theme
        // 'default', we have to use the default theme.
        if (Object.keys(themes).indexOf(theme) === -1 || theme === 'default' || !theme) {
            theme = default_theme;
        }

        // Save the theme
        Cookies.set('theme', theme);

        // Set the theme
        document.body.className = themes[theme].class;
    }
};
