const template = `
    <table class="table is-fullwidth responsive-table">
      <thead>
        <tr>
          <th>Token</th>
          <th>Expires</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="token in $store.state.tokens">
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
    `


function copyTokenUrl(token) {
    const registrationUrl = [location.origin, 'register', token.token].join('/');
    navigator.clipboard.writeText(registrationUrl);
}


function deleteToken(token) {
    fetch('/api/v1/registration/tokens/' + token.id, { method: 'DELETE' }).then(response => {
        if (response.ok) {
            this.$store.commit('deleteToken', token);
        } else if (response.headers.get('Content-Type').startsWith('application/json')) {
            response.json().then(console.error);
        } else {
            console.error(response);
        }
    });
}


export default {
    template,
    methods: { copyTokenUrl, deleteToken },
}
