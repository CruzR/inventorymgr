import { createQualification } from '/static/api.js'
import QualificationForm from '/static/views/qualificationform.js'

const template = `
    <qualification-form
      context="create"
      :error="errorMessage"
      @commit-qualification-change="sendCreateQualificationRequest">
    </qualification-form>`

function sendCreateQualificationRequest(qualification) {
    createQualification(qualification).then(response => {
        if (response.success) {
            this.$store.commit('updateQualification', response.data);
            this.$router.push('/qualifications');
        } else {
            console.error(response.error);
            this.errorMessage = this.$t(`errors.${response.error.reason}`);
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
