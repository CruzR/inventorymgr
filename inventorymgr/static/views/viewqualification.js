import { deleteQualification } from '/static/api.js'
import DeleteDialog from '/static/views/delete-dialog.js'
import QualificationForm from '/static/views/qualificationform.js'


const template = `
    <div>
      <delete-dialog
        :show="showDeleteDialog"
        @cancel-delete="showDeleteDialog = false"
        @commit-delete="sendDeleteQualificationRequest(currentQualification)">
        {{ $t('messages.delete_qualification', {name: currentQualification.name}) }}
      </delete-dialog>
      <qualification-form
        v-if="currentQualification"
        context="view"
        :current="currentQualification"
        @delete-qualification="showDeleteDialog = true">
      </qualification-form>
    </div>
    `

function currentQualification() {
    const path = location.pathname.split('/');
    const idComponent = path[path.length - 1];
    const id = parseInt(idComponent);
    return this.qualifications.find(q => q.id === id);
}

function sendDeleteQualificationRequest(qualification) {
    deleteQualification(qualification).then(response => {
        if (response.success) {
            location = location.origin + '/qualifications';
        } else {
            console.error(response.error);
            this.errorMessage = this.$t(`errors.${response.error.reason}`);
        }
    })
}

export default {
    template,
    props: ['qualifications'],
    data: () => {
        return { errorMessage: '', showDeleteDialog: false }
    },
    computed: {
        currentQualification,
    },
    methods: {
        sendDeleteQualificationRequest
    },
    components: {
        QualificationForm,
        DeleteDialog,
    }
}
