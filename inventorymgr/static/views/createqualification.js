import QualificationForm from '/static/views/qualificationform.js'

const template = `
    <qualification-form
      context="create"
      :error="errorMessage"
      @commit-qualification-change="sendCreateQualificationRequest">
    </qualification-form>`

function sendCreateQualificationRequest(qualification) {
    const headers = new Headers();
    headers.append('Content-Type', 'application/json;charset=UTF-8');
    const params = {
        method: 'POST',
        headers,
        body: JSON.stringify(qualification)
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
            errorMessage: ''
        }
    },
    methods: {
        sendCreateQualificationRequest
    },
    components: {
        QualificationForm
    }
}
