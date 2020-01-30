import { mapState } from '/static/vuex.esm.browser.js'
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
            this.errorMessage = this.$t(`errors.${response.error.reason}`);
        }
    })
}

export default {
    template,
    data: () => {
        return { errorMessage: '', showDeleteDialog: false }
    },
    computed: {
        currentQualification,
        ...mapState(['qualifications']),
    },
    methods: {
        sendDeleteQualificationRequest
    },
    components: {
        QualificationForm,
        DeleteDialog,
    }
}
