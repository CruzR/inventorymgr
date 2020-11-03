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
        if (response.success) {
            this.$store.commit('addItem', response.data);
            location = location.origin + '/items';
        } else {
            console.error(response.error);
            this.errorMessage = this.$t(`errors.${response.error.reason}`);
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
