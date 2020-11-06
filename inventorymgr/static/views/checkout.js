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
                  <datalist id="checkout-item-names">
                    <option v-for="item in items" :value="item.name"/>
                  </datalist>
                  <input
                    id="checkout-item"
                    autofocus
                    list="checkout-item-names"
                    class="input"
                    v-model="itemBarcodeOrName">
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
    const item = this.selectedItem;
    if (item) {
        const index = this.selected_items.findIndex(i => i.id === item.id);
        if (index !== -1) {
            this.selected_items.splice(index, 1);
        }
        this.selected_items.unshift(item);
        this.itemBarcodeOrName = '';
    }
}


function selectUser(e) {
    const user = this.selectedUser;
    if (user) {
        this.selected_user = user;
        this.userBarcodeOrName = '';
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
    props: ['users', 'items'],
    data: () => {
        return {
            errorMessage: '',
            itemBarcodeOrName: '',
            userBarcodeOrName: '',
            selected_items: [],
            selected_user: null,
        };
    },
    computed: {
        selectedItem: function() {
            const barcodeOrName = this.itemBarcodeOrName.trim();
            const itemByBarcode = this.items.find(i => i.barcode === barcodeOrName);
            return itemByBarcode || this.items.find(i => i.name === barcodeOrName);
        },
        selectedUser: function() {
            const barcodeOrName = this.userBarcodeOrName.trim();
            const userByBarcode = this.users.find(u => u.barcode === barcodeOrName);
            return userByBarcode || this.users.find(u => u.username === barcodeOrName);
        },
    },
    methods: { selectItem, selectUser, sendCheckoutRequest },
}
