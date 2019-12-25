const template = `
    <div>
      <div v-if="!readonly" class="field has-addons">
        <div class="control is-expanded">
          <div class="select is-fullwidth">
            <select v-model="selected">
              <option
                v-for="(choice, index) in choices"
                :value="index">{{ choice.name }}</option>
            </select>
          </div>
        </div>
        <div class="control">
          <button type="button" class="button" @click="addSelected">Add</button>
        </div>
      </div>
      <div class="tags">
        <span
          v-for="(item, index) in items"
          class="tag">
          {{ item.name }}
          <button
            v-if="!readonly"
            type="button"
            class="delete is-small"
            @click="removeAtIndex(index)"></button>
        </span>
      </div>
    </div>`


function addSelected() {
    const selected = this.choices[parseInt(this.selected)];
    const index = this.items.findIndex(i => i.name === selected.name);
    if (index === -1) {
        this.$emit('update:items', this.items.concat(selected));
    }
}


function removeAtIndex(index) {
    const upToIndex = this.items.slice(0, index);
    const afterIndex = this.items.slice(index + 1);
    this.$emit('update:items', upToIndex.concat(afterIndex));
}


export default {
    template,
    props: ['choices', 'readonly', 'items'],
    data: function() {
        return { selected: 0 };
    },
    methods: { addSelected, removeAtIndex },
}
