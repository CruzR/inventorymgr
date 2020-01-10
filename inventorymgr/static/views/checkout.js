import { mapState } from '/static/vuex.esm.browser.js'
import { checkout } from '/static/api.js'


const template = `
    <div>
      <div v-if="errorMessage" class="message is-danger">
        <div class="message-body">{{ errorMessage }}</div>
      </div>
      <div class="columns">
        <div class="column">
          <form @submit.prevent="selectItem">
            <div class="field">
              <label class="label" for="checkout-item">{{ $t('fields.item_barcode') }}</label>
              <div class="field has-addons">
                <div class="control is-expanded">
                  <input
                    id="checkout-item"
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
          <table v-if="selected_items.length" class="table is-fullwidth responsive-table">
            <thead>
              <tr>
                <th>{{ $t('fields.barcode') }}</th>
                <th>{{ $t('fields.item') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in selected_items">
                <td :data-label="$t('fields.barcode')">{{ item.barcode }}</td>
                <td :data-label="$t('fields.item')">{{ item.name }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="column">
          <form @submit.prevent="selectUser">
            <div class="field">
              <label class="label" for="checkout-user">{{ $t('fields.user_barcode') }}</label>
              <div class="field has-addons">
                <div class="control is-expanded">
                  <input
                    id="checkout-user"
                    class="input"
                    v-model="user_barcode">
                </div>
                <div class="control">
                  <button class="button">{{ $t('actions.add') }}</button>
                </div>
              </div>
            </div>
          </form>
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
      <form @submit.prevent="sendCheckoutRequest">
        <div class="field">
          <div class="control">
            <button class="button is-primary">{{ $t('actions.checkout') }}</button>
          </div>
        </div>
      </form>
    </div>`


function selectItem() {
    const item_barcode = this.item_barcode.trim();
    const item = this.items.find(i => i.barcode === item_barcode);
    if (item) {
        const index = this.selected_items.findIndex(i => i.id === item.id);
        if (index !== -1) {
            this.selected_items.splice(index, 1);
        }
        this.selected_items.unshift(item);
        this.item_barcode = '';
    }
}


function selectUser(e) {
    const barcode = this.user_barcode.trim();
    const user = this.users.find(u => u.barcode === barcode);
    if (user) {
        this.selected_user = user;
        this.user_barcode = '';
    }
}


function sendCheckoutRequest() {
    if (!this.selected_items.length) {
        this.errorMessage = 'Select an item to checkout';
        return;
    }

    if (!this.selected_user) {
        this.errorMessage = 'Select borrowing user';
        return;
    }

    this.errorMessage = '';

    const checkoutRequest = {
        borrowing_user_id: this.selected_user.id,
        borrowed_item_ids: this.selected_items.map(i => i.id),
    };

    checkout(checkoutRequest).then(response => {
        if (response.success) {
            this.$store.commit('addBorrowStates', response.data.borrowstates);
            this.selected_items = [];
            this.selected_user = null;
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
            item_barcode: '',
            user_barcode: '',
            selected_items: [],
            selected_user: null,
        };
    },
    computed: mapState(['items', 'users']),
    methods: { selectItem, selectUser, sendCheckoutRequest },
}
