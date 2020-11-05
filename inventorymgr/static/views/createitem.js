import { createItem } from '/static/api.js'
import ItemForm from '/static/views/itemform.js'


const template = `
    <item-form
      context="create"
      :error="errorMessage"
      :qualifications="qualifications"
      @commit-item-change="sendCreateItemRequest"
      @cancel-item-change="returnToDashboard">
    </item-form>`


function sendCreateItemRequest(item) {
    createItem(item).then(response => {
        if (response.success) {
            location = location.origin + '/items';
        } else {
            console.error(response.error);
            this.errorMessage = this.$t(`errors.${response.error.reason}`);
        }
    });
}


function returnToDashboard() {
    location = location.origin + '/';
}


export default {
    template,
    props: ['qualifications'],
    data: () => { return { errorMessage: '' } },
    methods: { sendCreateItemRequest, returnToDashboard },
    components: { ItemForm },
}
