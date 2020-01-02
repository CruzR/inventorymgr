import { createItem } from '/static/api.js'
import ItemForm from '/static/views/itemform.js'


const template = `
    <item-form
      context="create"
      :error="errorMessage"
      @commit-item-change="sendCreateItemRequest"
      @cancel-item-change="returnToDashboard">
    </item-form>`


function sendCreateItemRequest(item) {
    createItem(item).then(response => {
        if (response.success) {
            this.$store.commit('addItem', response.data);
            this.$router.push('/items');
        } else {
            console.error(response.error);
            this.errorMessage = response.error.message;
        }
    });
}


function returnToDashboard() {
    this.$router.push('/');
}


export default {
    template,
    data: () => { return { errorMessage: '' } },
    methods: { sendCreateItemRequest, returnToDashboard },
    components: { ItemForm },
}
