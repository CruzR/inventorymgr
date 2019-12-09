const template = `
    <div>
      <div v-if="errorMessage" class="message is-danger">
        <div class="message-body">
          {{ errorMessage }}
        </div>
      </div>
      <form @submit.prevent="$emit('commit-qualification-change', qualification)">
        <div class="field">
          <label class="label">Name</label>
          <div class="control">
            <input
              type="text" placeholder="Name"
              v-model="qualification.name">
          </div>
        </div>
        <div class="field">
          <div class="control">
            <button class="button is-primary" type="submit">
              Create
            </button>
          </div>
        </div>
      </form>
    </div>`

export default {
    template,
    slots: ['context'],
    data: () => {
        return {
            qualification: {
                name: ''
            },
            errorMessage: ''
        }
    },
}
