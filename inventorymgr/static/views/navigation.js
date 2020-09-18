import { logout } from '/static/api.js'


const navbarLinkTemplate = `
    <a
      :href="href"
      :class="{ 'navbar-item': true, 'is-active': isActive }">
      <slot></slot>
    </a>`


const NavbarLink = {
  props: ['href'],
  template: navbarLinkTemplate,
  computed: {
    isActive: function() {
      return location.pathname.startsWith(this.href);
    },
  },
};


const template = `
    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <a :class="{ 'navbar-item': true, 'is-active': isDashboard }" href="/">
          inventorymgr
        </a>
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
          <navbar-link
            v-if="sessionUser"
            href="/users/me">{{ sessionUser.username }}</navbar-link>
          <a class="navbar-item" @click="sendLogoutRequest">
            {{ $t('actions.logout') }}
          </a>
        </div>
      </div>
    </nav>`

function sendLogoutRequest() {
    logout().then(response => {
        if (response.success) {
            location = location.origin + '/login';
        } else {
            console.error(response.error);
        }
    });
}

export default {
    template,
    props: ['sessionUser'],
    data: () => {
        return {
            showMenu: false,
        }
    },
    methods: {
        sendLogoutRequest
    },
    computed: {
      isDashboard: () => location.pathname === '/',
    },
    components: { NavbarLink },
}
