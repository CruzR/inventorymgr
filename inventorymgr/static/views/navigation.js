const template = `
    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <div class="navbar-item">
          <router-link to="/">inventorymgr</router-link>
        </div>
        <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" @click="showMenu = !showMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>
      <div :class="{ 'navbar-menu': true, 'is-active': showMenu }">
        <div class="navbar-start">
          <div class="navbar-item">
            <router-link to="/users">Users</router-link>
          </div>
          <div class="navbar-item">
            <router-link to="/qualifications">Qualifications</router-link>
          </div>
        </div>
        <div class="navbar-end">
          <a class="navbar-item" @click="sendLogoutRequest">
            Logout
          </a>
        </div>
      </div>
    </nav>`

function sendLogoutRequest() {
    fetch('/api/v1/auth/logout', { method: 'POST' }).then(response => {
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
    methods: {
        sendLogoutRequest
    }
}
