import { mapState } from '/static/vuex.esm.browser.js'


const template = `
    <div>
      <table class="table is-fullwidth responsive-table">
        <thead>
          <tr>
            <th>Borrowing User</th>
            <th>Borrowed Item</th>
            <th>Received At</th>
            <th>Returned At</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="borrowstate in borrowstates">
            <td data-label="Borrowing User">
              {{ borrowstate.borrowing_user.username }}
            </td>
            <td data-label="Borrowed Item">
              {{ borrowstate.borrowed_item.name }}
            </td>
            <td data-label="Received At">
              {{ borrowstate.received_at }}
            </td>
            <td data-label="Returend At">
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
