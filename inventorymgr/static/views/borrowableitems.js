import { mapState } from '/static/vuex.esm.browser.js'


const template = `
    <div>
      <table class="table is-fullwidth responsive-table">
        <thead>
          <tr>
            <th>Item</th>
            <th>Barcode</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items">
            <td data-label="Item">{{ item.name }}</td>
            <td data-label="Barcode">{{ item.barcode }}</td>
            <td data-label="Actions">
              <div class="buttons">
                <router-link :to="'/items/' + item.id + '/edit'" v-slot="{ href, navigate }">
                  <a
                    :href="href"
                    class="button is-primary is-small"
                    @click="navigate">Edit</a>
                </router-link>
                <router-link :to="'/items/' + item.id" v-slot="{ href, navigate }">
                  <a
                    :href="href"
                    class="button is-small"
                    @click="navigate">View</a>
                </router-link>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>`


export default {
    template,
    computed: mapState(['items']),
}
