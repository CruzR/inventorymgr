import { register } from '/static/api.js'


const template = `
    <div class="columns is-centered section">
      <div class="column is-narrow">
        <h1 class="title">{{ $t('actions.register') }}</h1>
        <div v-if="error" class="message is-danger">
          <div class="message-body">
            {{ error }}
          </div>
        </div>
        <form class="box" @submit.prevent="sendRegistrationRequest">
          <div class="field">
            <label for="reg-username" class="label">{{ $t('fields.username') }}</label>
            <div class="control">
              <input required
                id="reg-username" type="text"
                class="input"
                v-model="newuser.username">
            </div>
          </div>
          <div class="field">
            <label for="reg-password" class="label">{{ $t('fields.password') }}</label>
            <div class="control">
              <input required
                id="reg-password" type="password"
                class="input"
                v-model="newuser.password">
            </div>
          </div>
          <div class="field">
            <label for="reg-repeat-password" class="label">
              {{ $t('fields.repeat_password') }}
            </label>
            <div class="control">
              <input required
                id="reg-repeat-password" type="password"
                class="input"
                v-model="newuser.repeat_password">
            </div>
          </div>
          <div class="field">
            <div class="control">
              <button type="submit" class="button is-primary">
                {{ $t('actions.register') }}
              </button>
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
    const token = this.$route.params.token;

    register(token, this.newuser).then(response => {
        if (response.success) {
            this.$router.push('/login');
        } else {
            console.error(response.error);
            this.error = this.$t(`errors.${response.error.reason}`);
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
