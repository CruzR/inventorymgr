import { mapState } from '/static/vuex.esm.browser.js'
import { logout } from '/static/api.js'


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
          <router-link to="/users" v-slot="{ href, navigate, isActive }">
            <a :class="{ 'navbar-item': true, 'is-active': isActive }" :href="href" @click="navigate">
              Users
            </a>
          </router-link>
          <router-link to="/qualifications" v-slot="{ href, navigate, isActive }">
            <a :class="{ 'navbar-item': true, 'is-active': isActive }" :href="href" @click="navigate">
              Qualifications
            </a>
          </router-link>
          <router-link to="/tokens" v-slot="{ href, navigate, isActive }">
            <a
              :class="{ 'navbar-item': true, 'is-active': isActive }"
              :href="href" @click="navigate">Invites</a>
          </router-link>
          <router-link to="/items" v-slot="{ href, navigate, isActive }">
            <a
              :class="{ 'navbar-item': true, 'is-active': isActive }"
              :href="href" @click="navigate">Inventory</a>
          </router-link>
        </div>
        <div class="navbar-end">
          <router-link
            v-if="sessionUser"
            to="/users/me"
            v-slot="{ href, navigate, isActive }">
            <a
              :href="href"
              :class="{ 'navbar-item': true, 'is-active': isActive }"
              @click="navigate">
              {{ sessionUser.username }}
            </a>
          </router-link>
          <a class="navbar-item" @click="sendLogoutRequest">
            Logout
          </a>
        </div>
      </div>
    </nav>`

function sendLogoutRequest() {
    logout().then(response => {
        if (response.status === 200) {
            this.$store.commit('logout');
            this.$router.push('/login');
        } else {
            console.error(response);
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
    }
}
