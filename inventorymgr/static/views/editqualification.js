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
            location = location.origin + '/qualifications';
        } else {
            console.error(response.error);
            this.errorMessage = this.$t(`errors.${response.error.reason}`);
        }
    })
}

function returnToView() {
    location = location.origin + '/qualifications/' + this.qualificationId;
}

function qualificationId() {
    const path = location.pathname.split('/');
    const idComponent = path[path.length - 2];
    return parseInt(idComponent);
}

function currentQualification() {
    const id = this.qualificationId;
    return this.qualifications.find(q => q.id === id);
}

export default {
    template,
    props: ['qualifications'],
    data: () => {
        return { errorMessage: '' }
    },
    computed: {
        currentQualification,
        qualificationId,
    },
    methods: {
        sendUpdateQualificationRequest,
        returnToView
    },
    components: {
        QualificationForm
    }
}
