import { mapState } from '/static/vuex.esm.browser.js'
import TagSelectBox from '/static/views/tagselectbox.js'

const template = `
    <div>
      <div v-if="error" class="message is-danger">
        <div class="message-body">
          {{ error }}
        </div>
      </div>
      <form @submit.prevent="$emit('commit-item-change', item)">
        <div class="field">
          <label class="label" for="item-name">{{ $t('fields.item') }}</label>
          <div class="control">
            <input id="item-name" type="text" required
              :readonly="isViewContext"
              :class="{ 'input': true, 'is-static': isViewContext }"
              v-model="item.name">
          </div>
        </div>
        <div v-if="!isCreateContext" class="field">
          <label class="label" for="item-barcode">{{ $t('fields.barcode') }}</label>
          <div class="control">
            <input id="item-barcode" type="text" readonly
              class="input is-static" :value="item.barcode">
          </div>
        </div>
        <div class="field">
          <label class="label">{{ $t('fields.required_qualifications') }}</label>
          <div class="control">
            <tag-select-box
              :items.sync="item.required_qualifications"
              :readonly="isViewContext"
              :choices="qualifications">
            </tag-select-box>
          </div>
        </div>
        <div v-if="isEditContext" class="field is-grouped">
          <div class="control">
            <button type="submit" class="button is-primary">{{ $t('actions.save') }}</button>
          </div>
          <div class="control">
            <button
              class="button" type="button"
              @click="$emit('cancel-item-change')">{{ $t('actions.cancel') }}</button>
          </div>
        </div>
        <div v-else-if="isViewContext" class="field is-grouped">
          <div class="control">
            <router-link
              :to="'/items/' + current.id + '/edit'" v-slot="{ href, navigate }">
              <a
                :href="href"
                class="button is-primary"
                @click="navigate">{{ $t('actions.edit') }}</a>
            </router-link>
          </div>
          <div class="control">
            <button
              type="button" class="button is-danger"
              @click="$emit('delete-item', current)">{{ $t('actions.delete') }}</button>
          </div>
        </div>
        <div v-else-if="isCreateContext" class="field is-grouped">
          <div class="control">
            <button type="submit" class="button is-primary">{{ $t('actions.create') }}</button>
          </div>
          <div class="control">
            <button
              class="button" type="button"
              @click="$emit('cancel-item-change')">{{ $t('actions.cancel') }}</button>
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
            : { name: '', barcode: '', required_qualifications: [] };
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
        ...mapState(['qualifications']),
    },
    components: { TagSelectBox },
}
