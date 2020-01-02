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
        if (response.success) {
            this.$store.commit('deleteQualification', qualification);
            this.$router.push('/qualifications');
        } else {
            console.error(response.error);
            this.errorMessage = response.error.message;
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
