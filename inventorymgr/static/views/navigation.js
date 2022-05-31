import { mapState } from '/static/vuex.esm.browser.js'
import { fetchBorrowStates, fetchItems, fetchUsers, logout } from '/static/api.js'


const navbarLinkTemplate = `
    <router-link :to="href" v-slot="{ href, navigate, isActive }">
      <a
        :href="href"
        :class="{ 'navbar-item': true, 'is-active': isActive }"
        @click="navigate"><slot></slot></a>
    </router-link>`


const NavbarLink = {
  props: ['href'],
  template: navbarLinkTemplate,
};


const template = `
    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <router-link to="/" v-slot="{ href, navigate, isExactActive }">
          <a :class="{ 'navbar-item': true, 'is-active': isExactActive }" :href="href" @click="navigate">
            inventorymgr
          </a>
        </router-link>
        <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" @click="showMenu = !showMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>
      <div :class="{ 'navbar-menu': true, 'is-active': showMenu }">
        <div class="navbar-start">
          <navbar-link href="/users">{{ $t('page.users') }}</navbar-link>
          <navbar-link href="/qualifications">{{ $t('page.qualifications') }}</navbar-link>
          <navbar-link href="/tokens">{{ $t('page.invites') }}</navbar-link>
          <navbar-link href="/items">{{ $t('page.inventory') }}</navbar-link>
          <navbar-link href="/checkout">{{ $t('page.checkout') }}</navbar-link>
          <navbar-link href="/checkin">{{ $t('page.checkin') }}</navbar-link>
          <navbar-link href="/borrowstates">{{ $t('page.borrowed_items') }}</navbar-link>
        </div>
        <div class="navbar-end">
          <div class="navbar-item">
            <button
              :class="{ 'button': true, 'is-info': true, 'is-outlined': true, 'is-loading': refreshingData }"
              title="Daten neuladen" @click="refreshData">🔄</button>
          </div>
          <navbar-link
            v-if="sessionUser"
            href="/users/me">{{ sessionUser.username }}</navbar-link>
          <a class="navbar-item" @click="sendLogoutRequest">
            {{ $t('actions.logout') }}
          </a>
        </div>
      </div>
    </nav>`

function refreshData() {
    this.refreshingData = true;
    Promise.all([fetchUsers(), fetchItems(), fetchBorrowStates()])
        .then(([usersResponse, itemsResponse, borrowStatesResponse]) => {
            let overallSuccess = true;
            if (usersResponse.success) {
                this.$store.commit('setUsers', usersResponse.data.users);
            } else {
                console.error(usersResponse.error);
                overallSuccess = false;
            }
            if (itemsResponse.success) {
                this.$store.commit('setItems', itemsResponse.data.items);
            } else {
                console.error(itemsResponse.error)
                overallSuccess = false;
            }
            if (borrowStatesResponse.success) {
                this.$store.commit('setBorrowStates', borrowStatesResponse.data.borrowstates);
            } else {
                console.error(borrowStatesResponse.error);
                overallSuccess = false;
            }
        })
        .catch(reason => { console.error(reason); })
        .then(() => { this.refreshingData = false; });
}


function sendLogoutRequest() {
    logout().then(response => {
        if (response.success) {
            this.$store.commit('logout');
            this.$router.push('/login');
        } else {
            console.error(response.error);
        }
    });
}

export default {
    template,
    data: () => {
        return {
            showMenu: false,
            refreshingData: false,
        }
    },
    computed: mapState(['sessionUser']),
    methods: {
        sendLogoutRequest,
        refreshData
    },
    components: { NavbarLink },
}
