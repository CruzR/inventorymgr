const template = `
    <div>
    <div v-if="errorMessage" class="message is-danger">
      <div class="message-body">
        {{ errorMessage }}
      </div>
    </div>
    <form @submit.prevent="sendCreateUserRequest">
      <div class="field">
        <label class="label">Username</label>
        <div class="control">
          <input
            type="text" placeholder="Username"
            v-model="user.username">
        </div>
      </div>
      <div class="field">
        <label class="label">Password</label>
        <div class="control">
          <input
            type="password" placeholder="Password"
            v-model="user.password">
        </div>
      </div>
      <fieldset class="field">
        <legend class="label">Permissions</legend>
        <div class="field">
          <label class="checkbox">
            <input type="checkbox" v-model="user.create_users">
            Create Users
          </label>
        </div>
        <div class="field">
          <label class="checkbox">
            <input type="checkbox" v-model="user.view_users">
            View Users
          </label>
        </div>
        <div class="field">
          <label class="checkbox">
            <input type="checkbox" v-model="user.update_users">
            Update Users
          </label>
        </div>
        <div class="field">
          <label class="checkbox">
            <input type="checkbox" v-model="user.edit_qualifications">
            Edit Qualifications
          </label>
        </div>
      </fieldset>
      <div class="field">
        <label class="label">Qualifications</label>
        <div class="control">
          <input type="text" placeholder="Qualifications">
        </div>
      </div>
      <div class="field">
        <div class="control">
          <button class="button is-primary" type="submit">Create</button>
        </div>
      </div>
    </form>
    </div>`

function sendCreateUserRequest() {
    const headers = new Headers();
    headers.append('Content-Type', 'application/json;charset=UTF-8');
    const params = {
        method: 'POST',
        headers,
        body: JSON.stringify(this.user)
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
        return {
            user: {
                username: '',
                password: '',
                create_users: false,
                view_users: false,
                update_users: false,
                edit_qualifications: false,
                qualifications: []
            },
            errorMessage: ''
        }
    },
    methods: {
        sendCreateUserRequest 
    }
}
