const template = `
    <div class="columns is-centered">
      <div class="column is-narrow">
        <h1 class="title">Login</h1>
        <div v-if="errorMessage" class="message is-danger">
          <div class="message-body">
            {{ errorMessage }}
          </div>
        </div>
        <form class="box" @submit.prevent="sendLoginRequest">
          <div class="field">
            <label class="label">Username</label>
            <div class="control">
              <input
                class="input" type="text" placeholder="Username"
                v-model="username">
            </div>
          </div>
          <div class="field">
            <label class="label">Password</label>
            <div class="control">
              <input
                class="input" type="password" placeholder="Password"
                v-model="password">
            </div>
          </div>
          <div class="field">
            <div class="control">
              <button
                  type="submit"
                  class="button is-primary">
                Login
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>`

function sendLoginRequest() {
    const headers = new Headers();
    headers.append('Content-Type', 'application/json;charset=UTF-8');
    const params = {
        method: 'POST',
        headers,
        body: JSON.stringify({
            username: this.username,
            password: this.password
        })
    };

    fetch('/api/v1/auth/login', params).then((response) => {
        if (response.status == 200) {
            window.is_authenticated = true;
            this.$store.commit('login');
            this.$router.push('/');
        } else {
            response.json().then((json) => {
                this.errorMessage = json.message;
            });
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
