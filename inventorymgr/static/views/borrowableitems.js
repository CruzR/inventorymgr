import { mapState } from '/static/vuex.esm.browser.js'
import RouterButton from '/static/views/routerbutton.js'


const template = `
    <div>
      <table class="table is-fullwidth responsive-table">
        <thead>
          <tr>
            <th>{{ $t('fields.item') }}</th>
            <th>{{ $t('fields.barcode') }}</th>
            <th>{{ $t('fields.required_qualifications') }}</th>
            <th>{{ $t('fields.actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items">
            <td :data-label="$t('fields.item')">{{ item.name }}</td>
            <td :data-label="$t('fields.barcode')">{{ item.barcode }}</td>
            <td :data-label="$t('fields.required_qualifications')">
              <div class="tags">
                <span
                  v-for="qualification in item.required_qualifications"
                  class="tag">
                  {{ qualification.name }}
                </span>
              </div>
            </td>
            <td :data-label="$t('fields.actions')">
              <div class="buttons">
                <router-button
                  :to="'/items/' + item.id + '/edit'" kind="is-primary is-small">
                  {{ $t('actions.edit') }}
                </router-button>
                <router-button :to="'/items/' + item.id" kind="is-small">
                  {{ $t('actions.view') }}
                </router-button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <router-button to="/items/new">
        {{ $t('actions.create_item') }}
      </router-button>
    </div>`


export default {
    template,
    computed: mapState(['items']),
    components: { RouterButton },
}
