import { mapState } from '/static/vuex.esm.browser.js'
import { deleteQualification } from '/static/api.js'
import QualificationForm from '/static/views/qualificationform.js'


const template = `
    <qualification-form
      v-if="currentQualification"
      context="view"
      :current="currentQualification"
      @delete-qualification="sendDeleteQualificationRequest">
    </qualification-form>`

function currentQualification() {
    const id = parseInt(this.$route.params.id);
    return this.qualifications.find(q => q.id === id);
}

function sendDeleteQualificationRequest(qualification) {
    deleteQualification(qualification).then(response => {
        if (response.ok) {
            this.$store.commit('deleteQualification', qualification);
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
        currentQualification,
        ...mapState(['qualifications']),
    },
    methods: {
        sendDeleteQualificationRequest
    },
    components: {
        QualificationForm
    }
}
