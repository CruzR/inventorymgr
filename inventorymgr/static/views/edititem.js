import { mapState } from '/static/vuex.esm.browser.js'
import { updateItem } from '/static/api.js'
import ItemForm from '/static/views/itemform.js'


const template = `
    <item-form
      v-if="currentItem"
      context="edit"
      :current="currentItem"
      :error="errorMessage"
      @commit-item-change="sendUpdateItemRequest"
      @cancel-item-change="cancelEdit">
    </item-form>`


function currentItem() {
    const id = parseInt(this.$route.params.id);
    return this.items.find(i => i.id === id);
}


function sendUpdateItemRequest(item) {
    updateItem(item).then(response => {
        if (response.ok) {
            response.json().then(item => {
                this.$store.commit('addItem', item);
                this.$router.push('/items');
            })
        } else if (response.headers.get('Content-Type').startsWith('application/json')) {
            response.json().then(error => {
                this.errorMessage = error.message;
                console.error(error);
            })
        } else {
            this.errorMessage = 'An error occurred during processing';
            console.error(response);
        }
    });
}


function cancelEdit() {
    this.$router.push('/items/' + this.$route.params['id'])
}

export default {
    template,
    data: () => {
        return { errorMessage: '' }
    },
    computed: { currentItem, ...mapState(['items']) },
    methods: { sendUpdateItemRequest, cancelEdit },
    components: { ItemForm },
}
