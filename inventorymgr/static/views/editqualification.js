import { mapState } from '/static/vuex.esm.browser.js'
import { updateQualification } from '/static/api.js'
import QualificationForm from '/static/views/qualificationform.js'


const template = `
    <qualification-form
      v-if="currentQualification"
      context="edit"
      :current="currentQualification"
      :error="errorMessage"
      @commit-qualification-change="sendUpdateQualificationRequest"
      @cancel-qualification-change="returnToView">
    </qualification-form>`

function sendUpdateQualificationRequest(qualification) {
    updateQualification(qualification).then(response => {
        if (response.success) {
            this.$store.commit('updateQualification', response.data);
            this.$router.push('/qualifications');
        } else {
            console.error(response.error);
            this.errorMessage = response.error.message;
        }
    })
}

function returnToView() {
    this.$router.push('/qualifications/' + this.$route.params.id);
}

function currentQualification() {
    const id = parseInt(this.$route.params.id);
    return this.qualifications.find(q => q.id === id);
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
        sendUpdateQualificationRequest,
        returnToView
    },
    components: {
        QualificationForm
    }
}
