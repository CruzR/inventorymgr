import { mapState } from '/static/vuex.esm.browser.js'
import { logout } from '/static/api.js'


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
          <navbar-link href="/users">Users</navbar-link>
          <navbar-link href="/qualifications">Qualifications</navbar-link>
          <navbar-link href="/tokens">Invites</navbar-link>
          <navbar-link href="/items">Inventory</navbar-link>
        </div>
        <div class="navbar-end">
          <navbar-link
            v-if="sessionUser"
            href="/users/me">{{ sessionUser.username }}</navbar-link>
          <a class="navbar-item" @click="sendLogoutRequest">
            Logout
          </a>
        </div>
      </div>
    </nav>`

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
        }
    },
    computed: mapState(['sessionUser']),
    methods: {
        sendLogoutRequest
    },
    components: { NavbarLink },
}
