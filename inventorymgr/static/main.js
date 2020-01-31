import Vue from '/static/vue.esm.browser.js'
import Vuex from '/static/vuex.esm.browser.js'
import { mapState } from '/static/vuex.esm.browser.js'
import VueI18n from '/static/vue-i18n.esm.browser.js'
import { messages } from '/static/messages.js'
import { fetchBorrowStates, fetchItems, fetchQualifications, fetchRegistrationTokens, fetchUser, fetchUsers } from '/static/api.js'
import VueRouter from '/static/vue-router.esm.browser.js'
import LoginView from '/static/views/login.js'
import CreateUserView from '/static/views/createuser.js'
import CreateQualificationView from '/static/views/createqualification.js'
import UsersView from '/static/views/users.js'
import QualificationsView from '/static/views/qualifications.js'
import NavigationBar from '/static/views/navigation.js'
import DashboardView from '/static/views/dashboard.js'
import EditUserView from '/static/views/edituser.js'
import UserDetailView from '/static/views/viewuser.js'
import QualificationDetailView from '/static/views/viewqualification.js'
import EditQualificationView from '/static/views/editqualification.js'
import RegistrationView from '/static/views/registration.js'
import RegistrationTokensView from '/static/views/tokens.js'
import BorrowableItemsView from '/static/views/borrowableitems.js'
import ItemDetailView from '/static/views/viewitem.js'
import ItemEditView from '/static/views/edititem.js'
import ItemCreateView from '/static/views/createitem.js'
import BorrowStatesList from '/static/views/borrowstates.js'
import CheckoutView from '/static/views/checkout.js'
import CheckinView from '/static/views/checkin.js'


Vue.config.errorHandler = (err, vm, info) => {
    handleError(err.message, err.fileName, err.lineNumber, err.columnNumber, err);
};

Vue.use(VueRouter);
Vue.use(Vuex);
Vue.use(VueI18n);

const routes = [
    { path: '/login', component: LoginView },
    { path: '/register/:token', component: RegistrationView },
    { path: '/', component: DashboardView },
    { path: '/users/new', component: CreateUserView },
    { path: '/users/:id', component: UserDetailView },
    { path: '/users/:id/edit', component: EditUserView },
    { path: '/users', component: UsersView },
    { path: '/qualifications/new', component: CreateQualificationView },
    { path: '/qualifications/:id', component: QualificationDetailView },
    { path: '/qualifications/:id/edit', component: EditQualificationView },
    { path: '/qualifications', component: QualificationsView },
    { path: '/tokens', component: RegistrationTokensView },
    { path: '/items', component: BorrowableItemsView },
    { path: '/items/new', component: ItemCreateView },
    { path: '/items/:id', component: ItemDetailView },
    { path: '/items/:id/edit', component: ItemEditView },
    { path: '/borrowstates', component: BorrowStatesList },
    { path: '/checkout', component: CheckoutView },
    { path: '/checkin', component: CheckinView },
];

const router = new VueRouter({
    mode: 'history',
    routes
});

const store = new Vuex.Store({
    state: {
        isAuthenticated: document.cookie == 'is_authenticated=1',
        users: [],
        qualifications: [],
        sessionUser: null,
        tokens: [],
        items: [],
        borrowstates: [],
    },
    mutations: {
        login: state => { state.isAuthenticated = true },
        logout: state => {
            state.isAuthenticated = false;
            state.users = [];
            state.qualifications = [];
            state.sessionUser = null;
            state.tokens = [];
            state.items = [];
            state.borrowstates = [];
        },
        setUsers: (state, users) => { state.users = users },
        setQualifications: (state, qualifications) => { state.qualifications = qualifications },
        setSessionUser: (state, user) => { state.sessionUser = user },
        updateUser: (state, user) => {
            const index = state.users.findIndex(u => u.id === user.id);
            if (index !== -1) {
                state.users.splice(index, 1, user);
            } else {
                state.users.push(user);
            }
        },
        deleteUser: (state, user) => {
            const index = state.users.findIndex(u => u.id === user.id);
            if (index !== -1) {
                state.users.splice(index, 1);
            }
        },
        updateQualification: (state, qualification) => {
            const index = state.qualifications.findIndex(q => q.id === qualification.id);
            if (index !== -1) {
                state.qualifications.splice(index, 1, qualification);
            } else {
                state.qualifications.push(qualification);
            }
        },
        deleteQualification: (state, qualification) => {
            const index = state.qualifications.findIndex(q => q.id === qualification.id);
            if (index !== -1) {
                state.qualifications.splice(index, 1);
            }
        },
        setTokens: (state, tokens) => {
            state.tokens = tokens;
        },
        deleteToken: (state, token) => {
            const index = state.tokens.findIndex(t => t.id === token.id);
            if (index !== -1) {
                state.tokens.splice(index, 1);
            }
        },
        addToken: (state, token) => {
            const index = state.tokens.findIndex(t => t.id === token.id);
            if (index === -1) {
                state.tokens.push(token);
            }
        },
        setItems: (state, items) => { state.items = items },
        addItem: (state, item) => {
            const index = state.items.findIndex(i => i.id === item.id);
            if (index === -1) {
                state.items.push(item);
            } else {
                state.items.splice(index, 1, item);
            }
        },
        deleteItem: (state, item) => {
            const index = state.items.findIndex(i => i.id === item.id);
            if (index !== -1) {
                state.items.splice(index, 1);
            }
        },
        setBorrowStates: (state, borrowstates) => { state.borrowstates = borrowstates },
        addBorrowStates: (state, borrowstates) => {
            for (let borrow_state of borrowstates) {
                const index = state.borrowstates.findIndex(b => b.id === borrow_state.id);
                if (index === -1) {
                    state.borrowstates.push(borrow_state);
                } else {
                    state.borrowstates.splice(index, 1, borrow_state);
                }
            }
        },
    }
});

router.beforeEach((to, from, next) => {
    if (!store.state.isAuthenticated) {
        if (to.path !== '/login' && !to.path.startsWith('/register')) {
            next({ path: '/login', query: { next: to.path } });
        } else {
            next();
        }
    } else {
        if (store.state.sessionUser === null) {
            fetchUser('me').then(response => {
                if (response.success) {
                    store.commit('setSessionUser', response.data)
                } else {
                    console.error(response.error);
                }
            })
        }
        if (!store.state.users.length) {
            fetchUsers().then(response => {
                if (response.success) {
                    store.commit('setUsers', response.data.users)
                } else {
                    console.error(response.error);
                }
            })
        }
        if (!store.state.qualifications.length) {
            fetchQualifications().then(response => {
                if (response.success) {
                    store.commit('setQualifications', response.data)
                } else {
                    console.error(response.error);
                }
            })
        }
        if (!store.state.tokens.length) {
            fetchRegistrationTokens().then(response => {
                if (response.success) {
                    store.commit('setTokens', response.data.tokens)
                } else {
                    console.error(response.error);
                }
            })
        }
        if (!store.state.items.length) {
            fetchItems().then(response => {
                if (response.success) {
                    store.commit('setItems', response.data.items)
                } else {
                    console.error(response.error)
                }
            })
        }
        if (!store.state.borrowstates.length) {
            fetchBorrowStates().then(response => {
                if (response.success) {
                    store.commit('setBorrowStates', response.data.borrowstates);
                } else {
                    console.error(response.error);
                }
            });
        }
        next();
    }
});

const i18n = new VueI18n({
    locale: navigator.language.slice(0, 2),
    messages,
});

const vm = new Vue({
    store,
    router,
    i18n,
    el: '#app',
    computed: mapState(['isAuthenticated']),
    components: {
        NavigationBar
    }
});
