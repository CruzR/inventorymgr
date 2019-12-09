import QualificationForm from '/static/views/qualificationform.js'

const template = `
    <qualification-form
      v-if="$store.state.qualifications.length"
      context="view"
      :current="currentQualification">
    </qualification-form>`

function currentQualification() {
    const id = parseInt(this.$route.params.id);
    return this.$store.state.qualifications.find(q => q.id === id);
}

export default {
    template,
    computed: {
        currentQualification
    },
    components: {
        QualificationForm
    }
}
