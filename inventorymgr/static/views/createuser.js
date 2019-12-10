import UserForm from '/static/views/userform.js'

const template = `
    <user-form
      context="create"
      :error="errorMessage"
      @commit-user-change="sendCreateUserRequest">
    </user-form>`

function sendCreateUserRequest(user) {
    const headers = new Headers();
    headers.append('Content-Type', 'application/json;charset=UTF-8');
    const params = {
        method: 'POST',
        headers,
        body: JSON.stringify(user)
    };

    fetch('/api/v1/users', params).then((response) => {
        if (response.status === 200) {
            this.$router.push('/');
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
