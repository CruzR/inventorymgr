import { mapState } from '/static/vuex.esm.browser.js'
import { checkin } from '/static/api.js'


const template = `
    <div>
      <div v-if="errorMessage" class="message is-danger">
        <div class="message-body">{{ errorMessage }}</div>
      </div>
      <form @submit.prevent="selectItem">
        <div class="field">
          <label class="label" for="checkin-item">{{ $t('fields.item_barcode') }}</label>
          <div class="field has-addons">
            <div class="control is-expanded">
              <input
                id="checkin-item"
                autofocus
                class="input"
                v-model="item_barcode">
            </div>
            <div class="control">
              <button class="button">{{ $t('actions.add') }}</button>
            </div>
          </div>
        </div>
      </form>
      <table
        v-if="selected_borrowstates.length"
        class="table is-fullwidth responsive-table">
        <thead>
          <tr>
            <th>{{ $t('fields.item') }}</th>
            <th>{{ $t('fields.borrowed_by') }}</th>
            <th>{{ $t('fields.received_at') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="borrow_state in selected_borrowstates">
            <td data-label="Item">{{ borrow_state.borrowed_item.name }}</td>
            <td data-label="Borrowed By">{{ borrow_state.borrowing_user.username }}</td>
            <td data-label="Received At">{{ borrow_state.received_at }}</td>
          </tr>
        </tbody>
      </table>
      <form @submit.prevent="sendCheckinRequest">
        <button class="button is-primary">{{ $t('actions.checkin') }}</button>
      </form>
    </div>`


function selectItem() {
    const selected_barcode = this.item_barcode.trim();
    const item = this.items.find(i => i.barcode === selected_barcode);
    if (!item) {
        this.errorMessage = 'Could not find item with that barcode.';
        return;
    }

    const borrowstates = this.borrowstates.filter(
      b => b.borrowed_item.id === item.id && b.returned_at === null);

    this.selected_borrowstates = borrowstates.concat(this.selected_borrowstates);
    this.item_barcode = '';
}


function sendCheckinRequest() {
    if (!this.selected_borrowstates.length) {
        this.errorMessage = 'Select at least one item.';
        return;
    }

    const item_ids = this.selected_borrowstates.map(b => b.borrowed_item.id);
    const checkinRequest = { item_ids };
    checkin(checkinRequest).then(response => {
        if (response.success) {
            this.$store.commit('addBorrowStates', response.data.borrowstates);
            this.$router.push('/borrowstates');
        } else {
            console.error(response.error);
            this.errorMessage = this.$t(`errors.${response.error.reason}`);
        }
    });
}


export default {
    template,
    data: () => {
        return { errorMessage: '', item_barcode: '', selected_borrowstates: [] };
    },
    computed: mapState(['borrowstates', 'items']),
    methods: { selectItem, sendCheckinRequest },
};