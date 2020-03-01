import { mapState } from '/static/vuex.esm.browser.js'
import LogList from '/static/views/log-list.js'
import UserBorrowedItems from '/static/views/user-borrowed-items.js'


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
      <h3 class="title is-4">{{ $t('fields.your_borrowed_items') }}</h3>
      <user-borrowed-items></user-borrowed-items>
      <h3 class="title is-4">{{ $t('fields.recent_activity') }}</h3>
      <log-list :logs="logs" v-if="users.length"></log-list>
    </section>`


export default {
    template,
    computed: mapState(['logs', 'users']),
    components: { LogList, UserBorrowedItems },
}
