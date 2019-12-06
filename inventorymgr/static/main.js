import Vue from '/static/vue.esm.browser.js'
import Vuex from '/static/vuex.esm.browser.js'
import VueRouter from '/static/vue-router.esm.browser.js'
import LoginView from '/static/views/login.js'
import CreateUserView from '/static/views/createuser.js'
import CreateQualificationView from '/static/views/createqualification.js'

Vue.use(VueRouter);
Vue.use(Vuex);

const DashboardView = { template: '<div>Dashboard</div>' };
const UsersView = { template: '<div>Users</div>' };

const routes = [
    { path: '/login', component: LoginView },
    { path: '/', component: DashboardView },
    { path: '/users/new', component: CreateUserView },
    { path: '/users', component: UsersView },
    { path: '/qualifications/new', component: CreateQualificationView },
];

const router = new VueRouter({
    mode: 'history',
    routes
});

const store = new Vuex.Store({
    state: {
        isAuthenticated: document.cookie == 'is_authenticated=1',
    },
    mutations: {
        login: state => { state.isAuthenticated = true },
    }
});

router.beforeEach((to, from, next) => {
    if (!store.state.isAuthenticated && to.path !== '/login') {
        next({ path: '/login', query: { next: to.path } });
    } else {
        next();
    }
});

const vm = new Vue({
    store,
    router,
    el: '#app'
});
