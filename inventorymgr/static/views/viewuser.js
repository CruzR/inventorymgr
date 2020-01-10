import { mapState } from '/static/vuex.esm.browser.js'
import { deleteUser } from '/static/api.js'
import UserForm from '/static/views/userform.js'

const template = `
    <user-form
      v-if="currentUser"
      :current="currentUser"
      context="view"
      @delete-user="sendDeleteUserRequest">
    </user-form>`

function currentUser() {
    if (this.$route.params.id === 'me') {
        return this.sessionUser;
    }
    const id = parseInt(this.$route.params.id);
    return this.users.find(u => u.id === id);
}

function sendDeleteUserRequest(user) {
    const id = this.$route.params.id;
    deleteUser(id).then(response => {
        if (response.success) {
            this.$store.commit('deleteUser', user);
            if (id === 'me') {
                this.$store.commit('logout');
                this.$router.push('/login');
            } else {
                this.$router.push('/users');
            }
        } else {
            console.error(response.error);
            this.errorMessage = this.$t(`errors.${response.error.reason}`);
        }
    })
}

export default {
    template,
    computed: {
        currentUser,
        ...mapState(['sessionUser', 'users']),
    },
    methods: {
        sendDeleteUserRequest
    },
    components: {
        UserForm
    }
}
