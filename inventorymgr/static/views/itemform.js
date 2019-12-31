const template = `
    <div>
      <div v-if="error" class="message is-danger">
        <div class="message-body">
          {{ error }}
        </div>
      </div>
      <form @submit.prevent="$emit('commit-item-change', item)">
        <div class="field">
          <label class="label" for="item-name">Item</label>
          <div class="control">
            <input id="item-name" type="text"
              :readonly="isViewContext"
              :class="{ 'input': true, 'is-static': isViewContext }"
              v-model="item.name">
          </div>
        </div>
        <div v-if="!isCreateContext" class="field">
          <label class="label" for="item-barcode">Barcode</label>
          <div class="control">
            <input id="item-barcode" type="text" readonly
              class="input is-static" :value="item.barcode">
          </div>
        </div>
        <div v-if="isEditContext" class="field is-grouped">
          <div class="control">
            <button type="submit" class="button is-primary">Save</button>
          </div>
          <div class="control">
            <button
              class="button" type="button"
              @click="$emit('cancel-item-change')">Cancel</button>
          </div>
        </div>
        <div v-else-if="isViewContext" class="field is-grouped">
          <div class="control">
            <router-link
              :to="'/items/' + current.id + '/edit'" v-slot="{ href, navigate }">
              <a
                :href="href"
                class="button is-primary"
                @click="navigate">Edit</a>
            </router-link>
          </div>
        </div>
        <div v-else-if="isCreateContext" class="field is-grouped">
          <div class="control">
            <button type="submit" class="button is-primary">Create</button>
          </div>
          <div class="control">
            <button
              class="button" type="button"
              @click="$emit('cancel-item-change')">Cancel</button>
          </div>
        </div>
      </form>
    </div>`


export default {
    props: ['current', 'context', 'error'],
    template,
    data: function() {
        const item = (typeof(this.current) !== 'undefined')
            ? JSON.parse(JSON.stringify(this.current))
            : { name: '', barcode: '' };
        return { item };
    },
    computed: {
        isViewContext: function() {
            return this.context == 'view';
        },
        isEditContext: function() {
            return this.context === 'edit';
        },
        isCreateContext: function() {
            return this.context === 'create';
        },
    },
}
