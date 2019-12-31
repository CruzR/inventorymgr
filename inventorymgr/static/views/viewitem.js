import { mapState } from '/static/vuex.esm.browser.js'
import ItemForm from '/static/views/itemform.js'

const template = `
    <item-form
      v-if="currentItem"
      context="view"
      :current="currentItem"
      :error="errorMessage"
      @delete-item="sendDeleteItemRequest">
    </item-form>`


function currentItem() {
    const id = parseInt(this.$route.params.id);
    return this.items.find(i => i.id === id);
}


function sendDeleteItemRequest(item) {
    const params = { method: 'DELETE' };
    fetch('/api/v1/items/' + item.id, params).then(response => {
        if (response.ok) {
            this.$store.commit('deleteItem', item);
            this.$router.push('/items');
        } else if (response.headers.get('Content-Type').startsWith('application/json')) {
            response.json().then(error => {
                console.error(error);
                this.errorMessage = error.message;
            });
        } else {
            console.error(response);
            this.errorMessage = "An error occured during processing.";
        }
    });
}


export default {
    template,
    data: () => { return { errorMessage: '' } },
    computed: { currentItem, ...mapState(['items']) },
    methods: { sendDeleteItemRequest },
    components: { ItemForm },
}
