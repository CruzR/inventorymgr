import Vue from '/static/vue.esm.browser.js'
import Vuex from '/static/vuex.esm.browser.js'
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

Vue.use(VueRouter);
Vue.use(Vuex);

const routes = [
    { path: '/login', component: LoginView },
    { path: '/', component: DashboardView },
    { path: '/users/new', component: CreateUserView },
    { path: '/users/:id', component: UserDetailView },
    { path: '/users/:id/edit', component: EditUserView },
    { path: '/users', component: UsersView },
    { path: '/qualifications/new', component: CreateQualificationView },
    { path: '/qualifications/:id', component: QualificationDetailView },
    { path: '/qualifications/:id/edit', component: EditQualificationView },
    { path: '/qualifications', component: QualificationsView },
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
    },
    mutations: {
        login: state => { state.isAuthenticated = true },
        logout: state => {
            state.isAuthenticated = false;
            state.users = [];
            state.qualifications = [];
            state.sessionUser = null;
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
    }
});

router.beforeEach((to, from, next) => {
    if (!store.state.isAuthenticated) {
        if (to.path !== '/login') {
            next({ path: '/login', query: { next: to.path } });
        } else {
            next();
        }
    } else {
        if (store.state.sessionUser === null) {
            fetch('/api/v1/users/me').then(response => {
                if (response.ok) {
                    response.json().then(user => {
                        store.commit('setSessionUser', user)
                    })
                } else {
                    if (response.headers.get('Content-Type').startsWith('application/json')) {
                        response.json().then(console.error);
                    } else {
                        console.error(response);
                    }
                }
            })
        }
        if (!store.state.users.length) {
            fetch('/api/v1/users').then(response => {
                if (response.ok) {
                    response.json().then(json => {
                        store.commit('setUsers', json.users)
                    })
                } else {
                    if (response.headers.get('Content-Type').startsWith('application/json')) {
                        response.json().then(console.error);
                    } else {
                        console.error(response);
                    }
                }
            })
        }
        if (!store.state.qualifications.length) {
            fetch('/api/v1/qualifications').then(response => {
                if (response.ok) {
                    response.json().then(qualifications => {
                        store.commit('setQualifications', qualifications)
                    })
                } else {
                    if (response.headers.get('Content-Type').startsWith('application/json')) {
                        response.json().then(console.error);
                    } else {
                        console.error(response);
                    }
                }
            })
        }
        next();
    }
});

const vm = new Vue({
    store,
    router,
    el: '#app',
    components: {
        NavigationBar
    }
});
