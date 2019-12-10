const template = `
    <div>
      <div v-if="error" class="message is-danger">
        <div class="message-body">
          {{ error }}
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
             <a :href="href" class="button is-primary" @click="navigate">
               Edit
             </a>
           </router-link>
          </div>
        </div>
      </form>
    </div>`

export default {
    template,
    props: ['context', 'current', 'error'],
    data: function() {
        const qualification = (typeof(this.current) !== 'undefined')
            ? JSON.parse(JSON.stringify(this.current))
            : { name: '' };

        return {
            qualification,
        }
    },
    computed: {
        isViewContext: function() {
            return this.context === 'view';
        }
    }
}
