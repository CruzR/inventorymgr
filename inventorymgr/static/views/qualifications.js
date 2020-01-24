import { mapState } from '/static/vuex.esm.browser.js'
import RouterButton from '/static/views/routerbutton.js'


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
                <router-button
                  :to="'/qualifications/' + qualification.id + '/edit'"
                  kind="is-primary is-small">
                  {{ $t('actions.edit') }}
                </router-button>
                <router-button
                  :to="'/qualifications/' + qualification.id" kind="is-small">
                  {{ $t('actions.view') }}
                </router-button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <router-button to="/qualifications/new">
        {{ $t('actions.create_qualification') }}
      </router-button>
    </div>
    `


export default {
    template,
    computed: mapState(['qualifications']),
    components: { RouterButton },
}
