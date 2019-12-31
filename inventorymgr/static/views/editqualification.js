import { mapState } from '/static/vuex.esm.browser.js'
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
    const headers = new Headers();
    headers.append('Content-Type', 'application/json;charset=UTF-8');
    const params = {
        method: 'PUT',
        headers,
        body: JSON.stringify(qualification)
    };

    fetch('/api/v1/qualifications/' + this.$route.params.id, params).then(response => {
        if (response.ok) {
            response.json().then(qualification => {
                this.$store.commit('updateQualification', qualification);
                this.$router.push('/qualifications');
            });
        } else if (response.headers.get('Content-Type').startsWith('application/json')) {
            response.json().then(error => {
                this.errorMessage = error.message;
                console.error(error);
            })
        } else {
            this.errorMessage = 'An error occurred during processing.';
            console.error(response);
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
