const template = `
    <div>
      <div v-if="errorMessage" class="message is-danger">
        <div class="message-body">
          {{ errorMessage }}
        </div>
      </div>
      <form @submit.prevent="sendCreateQualificationRequest">
        <div class="field">
          <label class="label">Name</label>
          <div class="control">
            <input
              type="text" placeholder="Name"
              v-model="qualification.name">
          </div>
        </div>
        <div class="field">
          <div class="control">
            <button class="button is-primary" type="submit">
              Create
            </button>
          </div>
        </div>
      </form>
    </div>`

function sendCreateQualificationRequest() {
    const headers = new Headers();
    headers.append('Content-Type', 'application/json;charset=UTF-8');
    const params = {
        method: 'POST',
        headers,
        body: JSON.stringify(this.qualification)
    };

    fetch('/api/v1/qualifications', params).then((response) => {
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
            qualification: {
                name: ''
            },
            errorMessage: ''
        }
    },
    methods: {
        sendCreateQualificationRequest
    }
}
