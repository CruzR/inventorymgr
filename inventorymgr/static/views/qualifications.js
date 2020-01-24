import { mapState } from '/static/vuex.esm.browser.js'


const template = `
    <div>
      <table class="table is-fullwidth responsive-table">
        <thead>
          <tr>
            <th>{{ $t('fields.qualification') }}</th>
            <th>{{ $t('fields.actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="qualification in qualifications">
            <td :data-label="$t('fields.qualification')">{{ qualification.name }}</td>
            <td :data-label="$t('fields.actions')">
              <div class="control">
                <router-link
                  :to="'/qualifications/' + qualification.id + '/edit'"
                  v-slot="{ href, navigate }">
                  <a :href="href" class="button is-primary is-small" @click="navigate">
                    {{ $t('actions.edit') }}
                  </a>
                </router-link>
                <router-link
                  :to="'/qualifications/' + qualification.id"
                  v-slot="{ href, navigate }">
                  <a :href="href" class="button is-primary is-small" @click="navigate">
                    {{ $t('actions.view') }}
                  </a>
                </router-link>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <router-link to="/qualifications/new" v-slot="{ href, navigate }">
        <a class="button" :href="href" @click="navigate">
          {{ $t('actions.create_qualification') }}
        </a>
      </router-link>
    </div>
    `


export default {
    template,
    computed: mapState(['qualifications']),
}
