import LogList from '/static/views/log-list.js'
import UserBorrowedItems from '/static/views/user-borrowed-items.js'
import IncomingTransferRequests from '/static/views/incoming-transfer-requests.js'


const template = `
    <section class="section">
      <nav class="tile is-ancestor has-text-centered">
        <div class="tile is-parent is-3">
          <a href="/users/new" class="tile is-child box">
            {{ $t('actions.create_user') }}
          </a>
        </div>
        <div class="tile is-parent is-3">
          <a href="/qualifications/new" class="tile is-child box">
            {{ $t('actions.create_qualification') }}
          </a>
        </div>
        <div class="tile is-parent is-3">
          <a href="/items/new" class="tile is-child box">
            {{ $t('actions.create_item') }}
          </a>
        </div>
      </nav>
      <h3 class="title is-4">{{ $t('fields.incoming_transfer_requests') }}</h3>
      <incoming-transfer-requests
        :borrowstates="borrowstates"
        :items="items"
        :session-user="sessionUser"
        :transfer-requests="transferRequests">
      </incoming-transfer-requests>
      <h3 class="title is-4">{{ $t('fields.your_borrowed_items') }}</h3>
      <user-borrowed-items
        :borrowstates="borrowstates"
        :items="items"
        :session-user="sessionUser"
        :users="users">
      </user-borrowed-items>
      <h3 class="title is-4">{{ $t('fields.recent_activity') }}</h3>
      <log-list
        :items="items"
        :logs="logs"
        :users="users"
         v-if="users.length">
      </log-list>
    </section>`


export default {
    template,
    props: ['logs', 'users', 'sessionUser', 'transferRequests', 'borrowstates', 'items'],
    components: { LogList, UserBorrowedItems, IncomingTransferRequests },
}
