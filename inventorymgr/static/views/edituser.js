import { mapState } from '/static/vuex.esm.browser.js'
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

    const headers = new Headers();
    headers.append('Content-Type', 'application/json;charset=UTF-8');
    const params = {
        method: 'PUT',
        headers,
        body: JSON.stringify(user)
    };

    fetch('/api/v1/users/' + this.$route.params.id, params).then(response => {
        if (response.ok) {
            response.json().then(user => {
                this.$store.commit('updateUser', user);
                if (this.$route.params.id === 'me') {
                    this.$store.commit('setSessionUser', user);
                }
                this.$router.push('/users');
            });
        } else if (response.headers.get('Content-Type').startsWith('application/json')) {
            response.json().then(error => {
                this.errorMessage = error.message;
                console.error(error);
            })
        } else {
            this.errorMessage = 'An error occurred during processing.';
            console.error(response);
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
