import { acceptTransferRequest, declineTransferRequest } from '/static/api.js'


const template = `
    <div>
      <table class="table is-fullwidth responsive-table">
        <thead>
          <tr>
            <th>{{ $t('fields.item') }}</th>
            <th>{{ $t('fields.actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in transferRequestsTable">
            <td>{{ row.item.name }}</td>
            <td>
              <div class="buttons">
                <button
                  type="button"
                  class="button is-primary is-small"
                  @click="onAcceptTransferRequest(row.transferRequest)">
                  {{ $t('actions.accept') }}
                </button>
                <button
                  type="button"
                  class="button is-small"
                  @click="onDeclineTransferRequest(row.transferRequest)">
                  {{ $t('actions.decline') }}
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    `


function onAcceptTransferRequest(transferRequest) {
    acceptTransferRequest(transferRequest).then(response => {
        if (response.success) {
            location = location.origin + '/';
        } else {
            console.error(response.error);
        }
    });
}

function onDeclineTransferRequest(transferRequest) {
    declineTransferRequest(transferRequest).then(response => {
        if (response.success) {
            location = location.origin + '/';
        } else {
            console.error(response.error);
        }
    });
}


function itemById(item_id) {
  return this.items.find(i => i.id === item_id);
}

function borrowstateById(id) {
  return this.borrowstates.find(bs => bs.id === id);
}

export default {
    template,
    props: ['sessionUser', 'transferRequests', 'items', 'borrowstates'],
    computed: {
        transferRequestsTable: function() {
            return this.transferRequests.map(tr => {
                const borrowState = this.borrowstateById(tr.borrowstate_id);
                const item = this.itemById(borrowState.borrowed_item.id);
                return {
                    transferRequest: tr,
                    borrowState,
                    item,
                };
            });
        },
    },
    methods: {
        onAcceptTransferRequest,
        onDeclineTransferRequest,
        itemById,
        borrowstateById,
    },
}
