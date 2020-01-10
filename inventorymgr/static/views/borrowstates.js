import { mapState } from '/static/vuex.esm.browser.js'


const template = `
    <div>
      <table class="table is-fullwidth responsive-table">
        <thead>
          <tr>
            <th>{{ $t('fields.item') }}</th>
            <th>{{ $t('fields.borrowed_by') }}</th>
            <th>{{ $t('fields.received_at') }}</th>
            <th>{{ $t('fields.returned_at') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="borrowstate in borrowstates">
            <td :data-label="$t('fields.item')">
              {{ borrowstate.borrowed_item.name }}
            </td>
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
    computed: mapState(['borrowstates']),
}
