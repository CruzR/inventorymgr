import UserForm from '/static/views/userform.js'

const template = `
    <user-form
      v-if="$store.state.users.length"
      :current="currentUser"
      context="view">
    </user-form>`

function currentUser() {
    const id = parseInt(this.$route.params.id);
    return this.$store.state.users.find(u => u.id === id);
}

export default {
    template,
    computed: {
        currentUser
    },
    components: {
        UserForm
    }
}
