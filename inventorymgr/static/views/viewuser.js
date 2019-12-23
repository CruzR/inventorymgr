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
        return this.$store.state.sessionUser;
    }
    const id = parseInt(this.$route.params.id);
    return this.$store.state.users.find(u => u.id === id);
}

function sendDeleteUserRequest(user) {
    const id = this.$route.params.id;
    fetch('/api/v1/users/' + id, { method: 'DELETE' }).then(response => {
        if (response.ok) {
            this.$store.commit('deleteUser', user);
            if (id === 'me') {
                this.$store.commit('logout');
                this.$router.push('/login');
            } else {
                this.$router.push('/users');
            }
        } else {
            if (response.headers.get('Content-Type').startsWith('application/json')) {
                response.json().then(error => {
                    console.error(error);
                    this.errorMessage = error.message;
                })
            } else {
                console.error(response);
                this.errorMessage = 'An error occurred during processing';
            }
        }
    })
}

export default {
    template,
    computed: {
        currentUser
    },
    methods: {
        sendDeleteUserRequest
    },
    components: {
        UserForm
    }
}
