const template = `
    <section class="section">
      <nav class="tile is-ancestor has-text-centered">
        <div class="tile is-parent is-2">
          <router-link to="/users/new" v-slot="{ href, navigate }">
            <a class="tile is-child box" :href="href" @click="navigate">
              Add User
            </a>
          </router-link>
        </div>
        <div class="tile is-parent is-2">
          <router-link to="/qualifications/new" v-slot="{ href, navigate }">
            <a class="tile is-child box" :href="href" @click="navigate">
              Add Qualification
            </a>
          </router-link>
        </div>
      </nav>
    </section>`

export default {
    template
}
