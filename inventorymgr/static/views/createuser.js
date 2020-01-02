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
        if (response.success) {
            this.$store.commit('updateUser', response.data);
            this.$router.push('/users');
        } else {
            console.error(response.error);
            this.errorMessage = response.error.message;
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
