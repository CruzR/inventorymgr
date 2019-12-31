import { createUser } from '/static/api.js'
import UserForm from '/static/views/userform.js'

const template = `
    <user-form
      context="create"
      :error="errorMessage"
      @commit-user-change="sendCreateUserRequest">
    </user-form>`

function sendCreateUserRequest(user, repeatedPassword) {
    if (user.password !== repeatedPassword) {
        this.errorMessage = 'Passwords do not match';
        return;
    }

    if (!user.password) {
        this.errorMessage = 'Password is empty';
        return;
    }

    createUser(user).then(response => {
        if (response.ok) {
            response.json().then(user => {
                this.$store.commit('updateUser', user);
                this.$router.push('/users');
            });
        } else if (response.status === 500) {
            this.errorMessage = 'An error occurred during processing.'
        } else {
            response.json().then((json) => {
                this.errorMessage = json.message;
            });
        }
    })
}

export default {
    template,
    data: () => {
        return { errorMessage: '' }
    },
    methods: {
        sendCreateUserRequest 
    },
    components: {
        UserForm
    }
}
