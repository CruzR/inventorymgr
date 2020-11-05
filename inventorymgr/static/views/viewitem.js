import { deleteItem } from '/static/api.js'
import DeleteDialog from '/static/views/delete-dialog.js'
import ItemForm from '/static/views/itemform.js'

const template = `
    <div>
      <delete-dialog
        :show="showDeleteDialog"
        @cancel-delete="showDeleteDialog = false"
        @commit-delete="sendDeleteItemRequest(currentItem)">
        {{ $t('messages.delete_item', {name: currentItem.name}) }}
      </delete-dialog>
      <item-form
        v-if="currentItem"
        context="view"
        :current="currentItem"
        :qualifications="qualifications"
        :error="errorMessage"
        @delete-item="showDeleteDialog = true">
      </item-form>
    </div>
    `


function itemId() {
    const path = location.pathname.split("/");
    return parseInt(path[path.length - 1]);
}


function currentItem() {
    const id = itemId();
    return this.items.find(i => i.id === id);
}


function sendDeleteItemRequest(item) {
    deleteItem(item).then(response => {
        if (response.success) {
            location = location.origin + '/items';
        } else {
            console.error(response.error);
            this.errorMessage = this.$t(`errors.${response.error.reason}`);
        }
    });
}


export default {
    template,
    props: ['items', 'qualifications'],
    data: () => { return { errorMessage: '', showDeleteDialog: false } },
    computed: { currentItem },
    methods: { sendDeleteItemRequest },
    components: { ItemForm, DeleteDialog },
}
