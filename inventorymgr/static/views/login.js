import { login } from '/static/api.js'


const template = `
    <div class="columns is-centered section">
      <div class="column is-narrow">
        <h1 class="title">{{ $t('actions.login') }}</h1>
        <div v-if="errorMessage" class="message is-danger">
          <div class="message-body">
            {{ errorMessage }}
          </div>
        </div>
        <form class="box" @submit.prevent="sendLoginRequest">
          <div class="field">
            <label class="label" for="login-username">{{ $t('fields.username') }}</label>
            <div class="control">
              <input id="login-username" class="input" type="text" v-model="username">
            </div>
          </div>
          <div class="field">
            <label class="label" for="login-password">{{ $t('fields.password') }}</label>
            <div class="control">
              <input
                id="login-password" class="input" type="password" v-model="password">
            </div>
          </div>
          <div class="field">
            <div class="control">
              <button
                  type="submit"
                  class="button is-primary">
                {{ $t('actions.login') }}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>`

function sendLoginRequest() {
    const user = { username: this.username, password: this.password };

    login(user).then(response => {
        if (response.success) {
            this.$store.commit('login');
            const nextRoute = this.$route.query['next'] || '/';
            this.$router.push(nextRoute);
        } else {
            console.error(response.error);
            this.errorMessage = this.$t(`errors.${response.error.reason}`);
        }
    })
}

export default {
    template,
    data: function() {
        return { username: '', password: '', errorMessage: '' };
    },
    methods: {
        sendLoginRequest
    }
}
