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
        <div class="field">
          <label class="label" for="item-barcode">Barcode</label>
          <div class="control">
            <input id="item-barcode" type="text" readonly
              class="input is-static" :value="item.barcode">
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
    },
}
