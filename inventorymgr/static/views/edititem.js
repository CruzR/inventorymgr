import { updateItem } from '/static/api.js'
import ItemForm from '/static/views/itemform.js'


const template = `
    <item-form
      v-if="currentItem"
      context="edit"
      :current="currentItem"
      :qualifications="qualifications"
      :error="errorMessage"
      @commit-item-change="sendUpdateItemRequest"
      @cancel-item-change="cancelEdit">
    </item-form>`


function itemId() {
    const path = location.pathname.split('/');
    const idComponent = path[path.length - 2];
    return parseInt(idComponent);
}

function currentItem() {
    const id = itemId();
    return this.items.find(i => i.id === id);
}


function sendUpdateItemRequest(item) {
    updateItem(item).then(response => {
        if (response.success) {
            location = location.origin + '/items';
        } else {
            console.error(response.error);
            this.errorMessage = this.$t(`errors.${response.error.reason}`);
        }
    });
}


function cancelEdit() {
    location = location.origin + '/items/' + this.currentItem.id;
}

export default {
    template,
    props: ['items', 'qualifications'],
    data: () => {
        return { errorMessage: '' }
    },
    computed: { currentItem },
    methods: { sendUpdateItemRequest, cancelEdit },
    components: { ItemForm },
}
