import { mapState } from '/static/vuex.esm.browser.js'
import { checkin } from '/static/api.js'


const template = `
    <div>
      <div v-if="errorMessage" class="message is-danger">
        <div class="message-body">{{ errorMessage }}</div>
      </div>
      <form @submit.prevent="selectUserOrItem">
        <div class="field">
          <label class="label" for="checkin-item">Barcode</label>
          <div class="field has-addons">
            <div class="control is-expanded">
              <datalist id="checkin-item-names">
                <option v-for="user in users" :value="user.username"/>
                <option v-for="item in items" :value="item.name"/>
              </datalist>
              <input
                id="checkin-item"
                v-autofocus
                list="checkin-item-names"
                class="input"
                v-model="userOrItem">
            </div>
            <div class="control">
              <button class="button">{{ $t('actions.add') }}</button>
            </div>
          </div>
        </div>
      </form>
      <!--
      <form @submit.prevent="selectUser">
        <div class="field">
          <label class="label" for="checkout-user">{{ $t('fields.user_barcode') }}</label>
          <div class="field has-addons">
            <div class="control is-expanded">
              <datalist id="checkout-user-names">
                <option v-for="user in users" :value="user.username"/>
              </datalist>
              <input
                id="checkout-user"
                list="checkout-user-names"
                class="input"
                v-model="userBarcodeOrName">
            </div>
            <div class="control">
              <button class="button">{{ $t('actions.add') }}</button>
            </div>
          </div>
        </div>
      </form>
      -->
      <div class="columns">
        <div class="column">
          <table
            v-if="selected_borrowstates.length"
            class="table is-fullwidth responsive-table">
            <thead>
              <tr>
                <th>{{ $t('fields.item') }}</th>
                <th>Anzahl</th>
                <th>{{ $t('fields.borrowed_by') }}</th>
                <th>{{ $t('fields.received_at') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="b in selected_borrowstates">
                <td :data-label="$t('fields.item')">{{ b.borrowstate.borrowed_item.name }}</td>
                <td data-label="Anzahl">{{ b.count }}</td>
                <td :data-label="$t('fields.borrowed_by')">{{ b.borrowstate.borrowing_user.username }}</td>
                <td :data-label="$t('fields.received_at')">{{ b.borrowstate.received_at }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="column">
          <table v-if="selected_user" class="table is-fullwidth responsive-table">
            <thead>
              <tr>
                <th>{{ $t('fields.user') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="selected_user">
                <td :data-label="$t('fields.user')">{{ selected_user.username }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <form @submit.prevent="sendCheckinRequest">
        <button class="button is-primary">{{ $t('actions.checkin') }}</button>
      </form>
    </div>`


function selectUserOrItem() {
    const userOrItem = this.selectedUserOrItem;
    if (!userOrItem) {
        this.errorMessage = 'Could not find user or item with that barcode.';
        return;
    }

    if (userOrItem.username) {
        this.selected_user = userOrItem;
        this.userOrItem = '';
        return;
    }

    const borrowstates = this.borrowstates.filter(
      b => b.borrowed_item.id === userOrItem.id && b.returned_at === null
    ).sort((a, b) => {
      const selected_user_id = this.selected_user?.id;
      if (a.borrowing_user.id == selected_user_id && b.borrowing_user.id != selected_user_id) {
        return -1;
      }
      if (b.borrowing_user.id == selected_user_id && a.borrowing_user.id != selected_user_id) {
        return 1;
      }
      if (a.received_at < b.received_at) return -1;
      if (b.received_at < a.received_at) return 1;
      return 0;
    })
    const newBorrowState = borrowstates.find(b => this.selected_borrowstates.findIndex(b0 => b0.borrowstate.id == b.id) == -1);
    if (!newBorrowState) return;


    this.selected_borrowstates.unshift({ borrowstate: newBorrowState, count: 1});
    this.userOrItem = '';
}


function sendCheckinRequest() {
    if (!this.selected_borrowstates.length) {
        this.errorMessage = 'Select at least one item.';
        return;
    }

    if (!this.selected_user) {
        this.errorMessage = 'Select returning user.';
        return;
    }

    const  user_id = this.selected_user.id;
    const item_ids = this.selected_borrowstates.map(b => { return { count: b.count, id: b.borrowstate.borrowed_item.id }; });
    const checkinRequest = { user_id, item_ids };
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
        return {
          errorMessage: '',
          userOrItem: '',
          selected_borrowstates: [],
          selected_user: null,
        };
    },
    computed: {
        selectedUserOrItem: function() {
            const barcodeOrName = this.userOrItem.trim();
            const userByBarcode = this.users.find(u => u.barcode === barcodeOrName);
            if (userByBarcode) return userByBarcode;
            const itemByBarcode = this.items.find(i => i.barcode === barcodeOrName);
            if (itemByBarcode) return itemByBarcode;
            return this.users.find(u => u.username === barcodeOrName) || this.items.find(i => i.name === barcodeOrName);
        },
        ...mapState(['borrowstates', 'items', 'users']),
    },
    methods: { selectUserOrItem, sendCheckinRequest },
};
