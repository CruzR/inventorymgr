const template = `
    <div class="columns is-centered section">
      <div class="column is-narrow">
        <h1 class="title">Register</h1>
        <div v-if="error" class="message is-danger">
          <div class="message-body">
            {{ error }}
          </div>
        </div>
        <form class="box" @submit.prevent="sendRegistrationRequest">
          <div class="field">
            <label for="reg-username" class="label">Username</label>
            <div class="control">
              <input required
                id="reg-username" type="text"
                class="input"
                v-model="newuser.username">
            </div>
          </div>
          <div class="field">
            <label for="reg-password" class="label">Password</label>
            <div class="control">
              <input required
                id="reg-password" type="password"
                class="input"
                v-model="newuser.password">
            </div>
          </div>
          <div class="field">
            <label for="reg-repeat-password" class="label">Repeat Password</label>
            <div class="control">
              <input required
                id="reg-repeat-password" type="password"
                class="input"
                v-model="newuser.repeat_password">
            </div>
          </div>
          <div class="field">
            <div class="control">
              <button type="submit" class="button is-primary">Register</button>
            </div>
          </div>
        </form>
      </div>
    </div>`


function formatError(error) {
    if (error.reason === 'invalid_token') {
        return 'Registration Token is invalid';
    } else if (error.reason === 'expired_token') {
        return 'Registration Token has expired';
    } else if (error.reason === 'password_mismatch') {
        return 'Passwords do not match';
    } else if (error.reason === 'missing_fields') {
        return ['Missing required fields:'].concat(error.missing).join(' ');
    } else {
        console.error(error);
        return 'Unknown error';
    }
}

function sendRegistrationRequest() {
    const headers = new Headers();
    headers.append('Content-Type', 'application/json');
    const params = {
        method: 'POST',
        headers,
        body: JSON.stringify(this.newuser),
    };

    const token = this.$route.params.token;

    fetch('/api/v1/registration/' + token, params).then(response => {
        if (response.ok) {
            this.$router.push('/login');
        } else if (response.headers.get('Content-Type').startsWith('application/json')) {
            response.json().then(formatError).then(error => {
                this.error = error;
            });
        } else {
            console.error(response);
            this.error = "An error occured during processing.";
        }
    });
}


export default {
    data: () => {
        return {
            'error': '',
            'newuser': { 'username': '', 'password': '', 'repeat_password': '' },
        }
    },
    template,
    methods: { sendRegistrationRequest },
}
