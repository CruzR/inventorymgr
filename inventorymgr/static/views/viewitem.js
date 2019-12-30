import ItemForm from '/static/views/itemform.js'

const template = `
    <item-form v-if="currentItem" context="view" :current="currentItem">
    </item-form>`


function currentItem() {
    const id = parseInt(this.$route.params.id);
    return this.$store.state.items.find(i => i.id === id);
}


export default {
    template,
    computed: { currentItem },
    components: { ItemForm },
}
