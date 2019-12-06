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
      </div>
    </nav>`

export default {
    template,
    data: () => {
        return {
            showMenu: false,
        }
    },
}
