import ItemForm from '/static/views/itemform.js'


const template = `
    <item-form
      context="create"
      :error="errorMessage"
      @commit-item-change="sendCreateItemRequest"
      @cancel-item-change="returnToDashboard">
    </item-form>`


function sendCreateItemRequest(item) {
    const headers = new Headers();
    headers.append('Content-Type', 'application/json');
    const params = {
        method: 'POST',
        headers,
        body: JSON.stringify(item)
    };
    fetch('/api/v1/items', params).then(response => {
        if (response.ok) {
            response.json().then(item => {
                this.$store.commit('addItem', item);
                this.$router.push('/items');
            });
        } else if (response.headers.get('Content-Type').startsWith('application/json')) {
            response.json().then(error => {
                console.error(error);
                this.errorMessage = error.message;
            });
        } else {
            console.error(response);
            this.errorMessage = "Error occurred during processing.";
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
