import { mapState } from '/static/vuex.esm.browser.js'


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
                <router-link :to="'/items/' + item.id + '/edit'" v-slot="{ href, navigate }">
                  <a
                    :href="href"
                    class="button is-primary is-small"
                    @click="navigate">{{ $t('actions.edit') }}</a>
                </router-link>
                <router-link :to="'/items/' + item.id" v-slot="{ href, navigate }">
                  <a
                    :href="href"
                    class="button is-small"
                    @click="navigate">{{ $t('actions.view') }}</a>
                </router-link>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <router-link to="/items/new" v-slot="{ href, navigate }">
        <a class="button" :href="href" @click="navigate">
          {{ $t('actions.create_item') }}
        </a>
      </router-link>
    </div>`


export default {
    template,
    computed: mapState(['items']),
}
