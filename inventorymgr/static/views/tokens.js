import { mapState } from '/static/vuex.esm.browser.js'
import { generateRegistrationToken, deleteRegistrationToken } from '/static/api.js'


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
    deleteRegistrationToken(token).then(response => {
        if (response.success) {
            this.$store.commit('deleteToken', token);
        } else {
            console.error(response.error);
            this.error = response.error.message;
        }
    });
}


function sendGenerateTokenRequest() {
    generateRegistrationToken().then(response => {
        if (response.success) {
            this.$store.commit('addToken', response.data);
        } else {
            console.error(response.error);
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
