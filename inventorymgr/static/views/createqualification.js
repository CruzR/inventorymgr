import { createQualification } from '/static/api.js'
import QualificationForm from '/static/views/qualificationform.js'

const template = `
    <qualification-form
      context="create"
      :error="errorMessage"
      @commit-qualification-change="sendCreateQualificationRequest">
    </qualification-form>`

function sendCreateQualificationRequest(qualification) {
    createQualification(qualification).then((response) => {
        if (response.ok) {
            response.json().then(qualification => {
                this.$store.commit('updateQualification', qualification);
                this.$router.push('/qualifications');
            });
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
