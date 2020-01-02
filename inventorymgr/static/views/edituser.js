import { mapState } from '/static/vuex.esm.browser.js'
import { updateUser } from '/static/api.js'
import UserForm from '/static/views/userform.js'


const template = `
    <user-form
      v-if="currentUser"
      :current="currentUser"
      :error="errorMessage"
      context="edit"
      @commit-user-change="sendUpdateUserRequest"
      @cancel-user-change="returnToUsers">
    </user-form>`

function sendUpdateUserRequest(user, repeatedPassword) {
    if ((user.password || repeatedPassword) && user.password !== repeatedPassword) {
        this.errorMessage = 'Passwords do not match';
        return;
    }

    if (!user.password) {
        delete user.password;
    }

    updateUser(this.$route.params.id, user).then(response => {
        if (response.success) {
            this.$store.commit('updateUser', response.data);
            if (this.$route.params.id === 'me') {
                this.$store.commit('setSessionUser', response.data);
            }
            this.$router.push('/users');
        } else {
            console.error(response.error);
            this.errorMessage = response.error.message;
        }
    })
}

function returnToUsers() {
    this.$router.push('/users/' + this.$route.params.id);
}

export default {
    template,
    data: () => {
        return { errorMessage: '' }
    },
    computed: {
        currentUser: function() {
            if (this.$route.params.id === 'me') {
                return this.sessionUser;
            }
            const id = parseInt(this.$route.params.id);
            return this.users.find(u => u.id === id);
        },
        ...mapState(['users', 'sessionUser']),
    },
    methods: {
        sendUpdateUserRequest,
        returnToUsers
    },
    components: {
        UserForm
    }
}
