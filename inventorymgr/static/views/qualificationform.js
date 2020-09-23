const template = `
    <div>
      <div v-if="error" class="message is-danger">
        <div class="message-body">
          {{ error }}
        </div>
      </div>
      <form @submit.prevent="$emit('commit-qualification-change', qualification)">
        <div class="field">
          <label class="label" for="qualificationform-name">{{ $t('fields.qualification') }}</label>
          <div class="control">
            <input
              id="qualificationform-name"
              type="text" required
              :readonly="isViewContext"
              :class="{ 'input': true, 'is-static': isViewContext }"
              v-model="qualification.name">
          </div>
        </div>
        <div class="field" v-if="context === 'create'">
          <div class="control">
            <button class="button is-primary" type="submit">
              {{ $t('actions.create') }}
            </button>
          </div>
        </div>
        <div class="field is-grouped" v-else-if="context === 'edit'">
          <div class="control">
            <button class="button is-primary" type="submit">
              {{ $t('actions.save') }}
            </button>
          </div>
          <div class="control">
            <button
              type="button"
              class="button"
              @click="$emit('cancel-qualification-change')">
              {{ $t('actions.cancel') }}
            </button>
          </div>
        </div>
        <div class="field is-grouped" v-else-if="isViewContext">
          <div class="control">
           <a :href="'/qualifications/' + current.id + '/edit'" class="button is-primary">
               {{ $t('actions.edit') }}
           </a>
          </div>
          <div class="control">
            <button type="button" class="button is-danger"
              @click="$emit('delete-qualification', current)">
              {{ $t('actions.delete') }}
            </button>
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
