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
        this.errorMessage = this.$t('errors.password_mismatch');
        return;
    }

    if (!user.password) {
        this.errorMessage = this.$t('errors.password_missing');
        return;
    }

    createUser(user).then(response => {
        if (response.success) {
            this.$store.commit('updateUser', response.data);
            this.$router.push('/users');
        } else {
            console.error(response.error);
            this.errorMessage = this.$t(`errors.${response.error.reason}`);
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
