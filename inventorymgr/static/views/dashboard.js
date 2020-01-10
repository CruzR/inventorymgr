const template = `
    <section class="section">
      <nav class="tile is-ancestor has-text-centered">
        <div class="tile is-parent is-3">
          <router-link to="/users/new" v-slot="{ href, navigate }">
            <a class="tile is-child box" :href="href" @click="navigate">
              {{ $t('actions.create_user') }}
            </a>
          </router-link>
        </div>
        <div class="tile is-parent is-3">
          <router-link to="/qualifications/new" v-slot="{ href, navigate }">
            <a class="tile is-child box" :href="href" @click="navigate">
              {{ $t('actions.create_qualification') }}
            </a>
          </router-link>
        </div>
        <div class="tile is-parent is-3">
          <router-link to="/items/new" v-slot="{ href, navigate }">
            <a class="tile is-child box" :href="href" @click="navigate">
              {{ $t('actions.create_item') }}
            </a>
          </router-link>
        </div>
      </nav>
    </section>`

export default {
    template
}
