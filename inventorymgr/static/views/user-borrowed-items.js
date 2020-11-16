import { transferItem } from '/static/api.js'


const template = `
    <div v-if="sessionUser !== null && borrowstates.length > 0 && items.length > 0">
      <table class="table is-fullwidth responsive-table">
        <thead>
          <tr>
            <th>{{ $t('fields.item') }}</t>
            <th>{{ $t('fields.received_at') }}</th>
            <th>{{ $t('fields.actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in borrowedItems">
            <td>{{ item.name }}</td>
            <td>{{ item.received_at }}</td>
            <td>
              <div class="buttons">
                <button class="button is-primary is-small" @click="showTransferDialog(item)">
		  {{ $t('actions.transfer') }}
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <div :class="{'modal': true, 'is-active': itemToTransfer !== null}" v-if="itemToTransfer !== null">
        <div class="modal-background"></div>
        <div class="modal-card">
          <header class="modal-card-head">
            <p class="modal-card-title">Transfer {{ itemToTransfer.name }}</p>
            <button class="delete" aria-label="close" @click="closeDialog"></button>
          </header>
          <section class="modal-card-body">
            <form id="user-borrowed-items-form" @submit.prevent="sendTransferItemRequest">
              <div class="field">
                <label class="label" for="user-borrowed-items-target-user">Transfer To</label>
                <div class="control">
                  <input id="user-borrowed-items-target-user" class="input" v-model="targetUserNameOrBarcode">
                </div>
              </div>
            </form>
          </section>
          <footer class="modal-card-foot">
            <button form="user-borrowed-items-form" class="button is-primary">Transfer</button>
            <button class="button" @click="closeDialog">Cancel</button>
          </footer>
        </div>
      </div>
    </div>
    `


function showTransferDialog(item) {
    this.itemToTransfer = item;
}

function closeDialog() {
    this.itemToTransfer = null;
    this.targetUserNameOrBarcode = "";
}

function sendTransferItemRequest() {
    let selectedUser = this.users.find(u => u.barcode === this.targetUserNameOrBarcode);
    if (!selectedUser) {
        selectedUser = this.users.find(u => u.username === this.targetUserNameOrBarcode);
    }
    if (!selectedUser) {
        return;
    }

    const this_ = this;
    transferItem({ borrowstate_id: this.itemToTransfer.borrowstate_id, target_user_id: selectedUser.id }).then(data => {
        if (!data.error) {
            this_.closeDialog();
        } else {
            console.error(data.error);
        }
    });
}


function itemById(item_id) {
  return this.items.find(i => i.id === item_id);
}

export default {
    template,
    props: ['borrowstates', 'sessionUser', 'users', 'items'],
    data: function() {
        return { itemToTransfer: null, targetUserNameOrBarcode: '' };
    },
    computed: {
        borrowedItems: function() {
            const userId = this.sessionUser.id;
            const itemById = this.itemById;
            return this.borrowstates
                .filter(bs => bs.borrowing_user.id === userId && bs.returned_at === null)
                .map(bs => {
                    return {
                        borrowstate_id: bs.id,
                        name: itemById(bs.borrowed_item.id).name,
                        received_at: bs.received_at
                    };
                });
        },
    },
    methods: {
        closeDialog,
        showTransferDialog,
        sendTransferItemRequest,
        itemById,
    },
}
