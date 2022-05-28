import { mapState } from '/static/vuex.esm.browser.js'
import { checkout } from '/static/api.js'


const template = `
    <div>
      <div v-if="errorMessage" class="message is-danger">
        <div class="message-body">{{ errorMessage }}</div>
      </div>
      <form @submit.prevent="selectUserOrItem">
        <div class="field">
          <label class="label" for="checkout-item">Barcode</label>
          <div class="field has-addons">
            <div class="control is-expanded">
              <datalist id="checkout-item-names">
                <option v-for="user in users" :value="user.username"/>
                <option v-for="item in items" :value="item.name"/>
              </datalist>
              <input
                id="checkout-item"
                autofocus
                list="checkout-item-names"
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
          <table v-if="selected_items.length" class="table is-fullwidth responsive-table">
            <thead>
              <tr>
                <th>{{ $t('fields.barcode') }}</th>
                <th>{{ $t('fields.item') }}</th>
                <th>Anzahl</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="i in selected_items">
                <td :data-label="$t('fields.barcode')">{{ i.item.barcode }}</td>
                <td :data-label="$t('fields.item')">{{ i.item.name }}</td>
                <td data-label="Anzahl">{{ i.count }}</td>
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
      <form @submit.prevent="sendCheckoutRequest">
        <div class="field">
          <div class="control">
            <button class="button is-primary">{{ $t('actions.checkout') }}</button>
          </div>
        </div>
      </form>
    </div>`


function selectUserOrItem() {
    const userOrItem = this.selectedUserOrItem;
    if (userOrItem?.username) {
        this.selected_user = userOrItem;
        this.userOrItem = '';
        return;
    }
    if (userOrItem) {
        const index = this.selected_items.findIndex(i => i.item.id === userOrItem.id);
        if (index !== -1) {
            this.selected_items[index].count += 1;
            // this.selected_items.splice(index, 1);
        } else {
            this.selected_items.unshift({item: userOrItem, count: 1});
        }
        this.userOrItem = '';
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
        borrowed_item_ids: this.selected_items.map(i => { return {id: i.item.id, count: i.count} }),
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
            userOrItem: '',
            selected_items: [],
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
        selectedUser: function() {
        },
        ...mapState(['items', 'users']),
    },
    methods: { selectUserOrItem, sendCheckoutRequest },
}
