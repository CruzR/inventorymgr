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

Vue.use(VueRouter);
Vue.use(Vuex);

const routes = [
    { path: '/login', component: LoginView },
    { path: '/', component: DashboardView },
    { path: '/users/new', component: CreateUserView },
    { path: '/users', component: UsersView },
    { path: '/qualifications/new', component: CreateQualificationView },
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
        qualifications: []
    },
    mutations: {
        login: state => { state.isAuthenticated = true },
        logout: state => { state.isAuthenticated = false },
        setUsers: (state, users) => { state.users = users },
        setQualifications: (state, qualifications) => { state.qualifications = qualifications },
    }
});

router.beforeEach((to, from, next) => {
    if (!store.state.isAuthenticated && to.path !== '/login') {
        next({ path: '/login', query: { next: to.path } });
    } else {
        if (!store.state.users.length) {
            fetch('/api/v1/users')
                .then(response => {
                    if (response.status === 500) {
                        console.error(response);
                    } else {
                        response.json().then(json => {
                            store.commit('setUsers', json.users)
                        })
                    }
                })
        }
        if (!store.state.users.length) {
            fetch('/api/v1/qualifications').then(response => {
                if (response.status === 500) {
                    console.error(response);
                } else {
                    response.json().then(qualifications => {
                        store.commit('setQualifications', qualifications)
                    })
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
