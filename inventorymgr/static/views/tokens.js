import { mapState } from '/static/vuex.esm.browser.js'


const template = `
    <div>
      <div v-if="error" class="message is-danger">
        <div class="message-body">
          {{ error }}
        </div>
      </div>
      <table class="table is-fullwidth responsive-table">
        <thead>
          <tr>
            <th>Token</th>
            <th>Expires</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="token in tokens">
            <td data-label="Token">{{ token.token }}</td>
            <td data-label="Expires">{{ token.expires }}</td>
            <td data-label="Actions">
              <div class="buttons">
                <button type="button" class="button is-small"
                  @click="copyTokenUrl(token)">Copy</button>
                <button type="button" class="button is-danger is-small"
                  @click="deleteToken(token)">Delete</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="field is-grouped is-grouped-right">
        <div class="control">
          <button type="button" class="button"
            @click="sendGenerateTokenRequest">Generate Token</button>
        </div>
      </div>
    </div>`


function copyTokenUrl(token) {
    const registrationUrl = [location.origin, 'register', token.token].join('/');
    navigator.clipboard.writeText(registrationUrl);
}


function deleteToken(token) {
    fetch('/api/v1/registration/tokens/' + token.id, { method: 'DELETE' }).then(response => {
        if (response.ok) {
            this.$store.commit('deleteToken', token);
        } else if (response.headers.get('Content-Type').startsWith('application/json')) {
            response.json().then(error => {
                this.error = 'Error: ' + error.reason;
                console.error(error);
            });
        } else {
            this.error = "An error occured during processing.";
            console.error(response);
        }
    });
}


function sendGenerateTokenRequest() {
    fetch('/api/v1/registration/tokens', { method: 'POST' }).then(response => {
        if (response.ok) {
            response.json().then(token => {
                this.$store.commit('addToken', token);
            });
        } else if (response.headers.get('Content-Type').startsWith('application/json')) {
            response.json().then(console.error);
        } else {
            console.error(response);
        }
    });
}


export default {
    template,
    data: () => {
        return { error: '' }
    },
    computed: mapState(['tokens']),
    methods: { copyTokenUrl, deleteToken, sendGenerateTokenRequest },
}
