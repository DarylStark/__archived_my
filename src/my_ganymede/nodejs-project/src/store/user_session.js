// Store to save user session information
export default {
    state() {
        return {
            user_fullname: null,
            session: {
                'account': {},
                'session': {}
            }
        }
    },
    mutations: {
        set_session(state, session) {
            console.log('setting session');
            state.session.account = session.user_account;
            state.session.session = session.session;
        }
    }
};