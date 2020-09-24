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
            <th>{{ $t('fields.token') }}</th>
            <th>{{ $t('fields.expires') }}</th>
            <th>{{ $t('fields.actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="token in tokens">
            <td :data-label="$t('fields.token')">{{ token.token }}</td>
            <td :data-label="$t('fields.expires')">{{ token.expires }}</td>
            <td :data-label="$t('fields.actions')">
              <div class="buttons">
                <button type="button" class="button is-small"
                  @click="copyTokenUrl(token)">{{ $t('actions.copy') }}</button>
                <button type="button" class="button is-danger is-small"
                  @click="deleteToken(token)">{{ $t('actions.delete') }}</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="field is-grouped is-grouped-right">
        <div class="control">
          <button type="button" class="button"
            @click="sendGenerateTokenRequest">{{ $t('actions.generate_token') }}</button>
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
            location = location;
        } else {
            console.error(response.error);
            this.error = this.$t(`errors.${response.error.reason}`);
        }
    });
}


function sendGenerateTokenRequest() {
    generateRegistrationToken().then(response => {
        if (response.success) {
            location = location;
        } else {
            console.error(response.error);
        }
    });
}


export default {
    template,
    props:['tokens'],
    data: () => {
        return { error: '' }
    },
    methods: { copyTokenUrl, deleteToken, sendGenerateTokenRequest },
}
