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
            <input
              v-if="isViewContext"
              id="item-name"
              type="text" required
              readonly
              class="input is-static"
              v-model="item.name">
            <input
              v-else
              v-autofocus
              id="item-name"
              type="text" required
              class="input"
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
          <label class="label" for="item-quantity-total">Anzahl Gesamt</label>
          <div class="control">
            <input id="item-quantity-total" required :readonly="isViewContext" :class="{ 'input': true, 'is-static': isViewContext }" v-model="item.quantity_total">
          </div>
        </div>
        <div class="field">
          <label class="label" for="item-quantity-in-stock">Anzahl auf Lager</label>
          <div class="control">
            <input id="item-quantity-in-stock" required :readonly="isViewContext" :class="{ 'input': true, 'is-static': isViewContext }" v-model="item.quantity_in_stock">
          </div>
        </div>
        <div class="field">
          <label class="label" for="item-unmatched-returns">Unbekannte R&uuml;ckgaben</label>
          <div class="control">
            <input id="item-unmatched-returns" required :readonly="isViewContext" :class="{ 'input': true, 'is-static': isViewContext }" v-model="item.unmatched_returns">
          </div>
        </div>
        <div class="field">
          <label class="label" for="item-description">Anmerkungen</label>
          <div class="control">
            <textarea id="item-description" :readonly="isViewContext" :class="{ 'textarea': true, 'is-static': isViewContext }" v-model="item.description"></textarea>
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
            : { name: '', barcode: '', quantity_total: 1, quantity_in_stock: 1, unmatched_returns: 0, description: '', required_qualifications: [] };
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
