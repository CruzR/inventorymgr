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
              :readonly="isViewContext"
              :class="{ 'input': true, 'is-static': isViewContext }"
              v-model="qualification.name">
          </div>
        </div>
        <div class="field" v-if="context === 'create'">
          <div class="control">
            <button class="button is-primary" type="submit">
              Create
            </button>
          </div>
        </div>
        <div class="field is-grouped" v-else-if="context === 'edit'">
          <div class="control">
            <button class="button is-primary" type="submit">
              Save
            </button>
          </div>
          <div class="control">
            <button
              type="button"
              class="button"
              @click="$emit('cancel-qualification-change')">
              Cancel
            </button>
          </div>
        </div>
        <div class="field" v-else-if="isViewContext">
          <div class="control">
           <router-link
             :to="'/qualifications/' + current.id + '/edit'"
             v-slot="{ href, navigate }">
             <a :href="href" class="button is-primary">
               Edit
             </a>
           </router-link>
          </div>
        </div>
      </form>
    </div>`

export default {
    template,
    props: ['context', 'current'],
    data: function() {
        const qualification = (typeof(this.current) !== 'undefined')
            ? JSON.parse(JSON.stringify(this.current))
            : { name: '' };

        return {
            qualification,
            errorMessage: ''
        }
    },
    computed: {
        isViewContext: function() {
            return this.context === 'view';
        }
    }
}
