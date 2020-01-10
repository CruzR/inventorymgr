import { mapState } from '/static/vuex.esm.browser.js'


const template = `
    <table class="table is-fullwidth responsive-table">
      <thead>
        <tr>
          <th>{{ $t('fields.username') }}</th>
          <th><abbr :title="$t('permissions.create_users')">👤✨</abbr></th>
          <th><abbr :title="$t('permissions.view_users')">👤🔍</abbr></th>
          <th><abbr :title="$t('permissions.update_users')">👤✏️</abbr></th>
          <th><abbr :title="$t('permissions.edit_qualifications')">🎓✏️</abbr></th>
          <th><abbr :title="$t('permissions.create_items')">🧰✏️</abbr></th>
          <th><abbr :title="$t('permissions.manage_checkouts')">🧰👋</abbr></th>
          <th>{{ $t('fields.qualifications') }}</th>
          <th>{{ $t('fields.actions') }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users">
          <td :data-label="$t('fields.username')">{{ user.username }}</td>
          <td :data-label="$t('permissions.create_users')">
            <input type="checkbox" :checked="user.create_users" disabled>
          </td>
          <td :data-label="$t('permissions.view_users')">
            <input type="checkbox" :checked="user.view_users" disabled>
          </td>
          <td :data-label="$t('permissions.update_users')">
            <input type="checkbox" :checked="user.update_users" disabled>
          </td>
          <td :data-label="$t('permissions.edit_qualifications')">
            <input type="checkbox" :checked="user.edit_qualifications" disabled>
          </td>
          <td :data-label="$t('permissions.create_items')">
            <input type="checkbox" :checked="user.create_items" disabled>
          </td>
          <td :data-label="$t('permissions.manage_checkouts')">
            <input type="checkbox" :checked="user.manage_checkouts" disabled>
          </td>
          <td :data-label="$t('fields.qualifications')">
            <div class="tags">
              <span
                v-for="qualification in user.qualifications"
                class="tag">
                {{ qualification.name }}
              </span>
            </div>
          </td>
          <td :data-label="$t('fields.actions')">
            <div class="control">
              <router-link
                :to="'/users/' + user.id + '/edit'"
                v-slot="{ href, navigate }">
                <a class="button is-primary is-small" :href="href" @click="navigate">
                  {{ $t('actions.edit') }}
                </a>
              </router-link>
              <router-link
                :to="'/users/' + user.id"
                v-slot="{ href, navigate }">
                <a class="button is-primary is-small" :href="href" @click="navigate">
                  {{ $t('actions.view') }}
                </a>
              </router-link>
            </div>
          </td>
        </tr>
      </tbody>
    </table>`


export default {
    template,
    computed: mapState(['users']),
}
