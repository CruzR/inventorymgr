import { mapState } from '/static/vuex.esm.browser.js'


const template = `
    <div>
      <div class="field is-grouped is-grouped-right">
        <label class="checkbox">
          <input type="checkbox" v-model="showReturned">
          {{ $t('actions.show_returned') }}
        </label>
      </div>
      <table class="table is-fullwidth responsive-table">
        <thead>
          <tr>
            <th>{{ $t('fields.item') }}</th>
            <th>Anzahl</th>
            <th>{{ $t('fields.borrowed_by') }}</th>
            <th>{{ $t('fields.received_at') }}</th>
            <th>{{ $t('fields.returned_at') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="borrowstate in filteredItems">
            <td :data-label="$t('fields.item')">
              {{ borrowstate.borrowed_item.name }}
            </td>
            <td data-label="Anzahl">{{ borrowstate.quantity }}</td>
            <td :data-label="$t('fields.borrowed_by')">
              {{ borrowstate.borrowing_user.username }}
            </td>
            <td :data-label="$t('fields.received_at')">
              {{ borrowstate.received_at }}
            </td>
            <td :data-label="$t('fields.returned_at')">
              {{ borrowstate.returned_at }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>`


export default {
    template,
    data: () => { return { showReturned: false } },
    computed: {
        filteredItems: function() {
            if (this.showReturned) {
                return this.borrowstates;
            }
            return this.borrowstates.filter(b => b.returned_at === null);
        },
        ...mapState(['borrowstates']),
    },
}
