import QualificationForm from '/static/views/qualificationform.js'

const template = `
    <qualification-form
      v-if="$store.state.qualifications.length"
      context="view"
      :current="currentQualification"
      @delete-qualification="sendDeleteQualificationRequest">
    </qualification-form>`

function currentQualification() {
    const id = parseInt(this.$route.params.id);
    return this.$store.state.qualifications.find(q => q.id === id);
}

function sendDeleteQualificationRequest(qualification) {
    const id = parseInt(this.$route.params.id);
    const headers = new Headers();
    headers.append('Content-Type', 'application/json;charset=UTF-8');
    const params = {
        method: 'DELETE',
        headers,
        body: JSON.stringify(qualification)
    };
    fetch('/api/v1/qualifications/' + id, params).then(response => {
        if (response.ok) {
            this.$router.push('/qualifications');
        } else {
            if (response.headers.get('Content-Type').startsWith('application/json')) {
                response.json().then(error => {
                    console.error(error);
                    this.errorMessage = error.message;
                })
            } else {
                console.error(response);
                this.errorMessage = 'An error occurred during processing';
            }
        }
    })
}

export default {
    template,
    data: () => {
        return { errorMessage: '' }
    },
    computed: {
        currentQualification
    },
    methods: {
        sendDeleteQualificationRequest
    },
    components: {
        QualificationForm
    }
}
