import { mapState } from '/static/vuex.esm.browser.js'
import { deleteItem } from '/static/api.js'
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
    deleteItem(item).then(response => {
        if (response.success) {
            this.$store.commit('deleteItem', item);
            this.$router.push('/items');
        } else {
            console.error(response.error);
            this.errorMessage = this.$t(`errors.${response.error.reason}`);
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
