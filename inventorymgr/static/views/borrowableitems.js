const template = `
    <div>
      <table class="table is-fullwidth responsive-table">
        <thead>
          <tr>
            <th>{{ $t('fields.item') }}</th>
            <th>{{ $t('fields.barcode') }}</th>
            <th>{{ $t('fields.required_qualifications') }}</th>
            <th>{{ $t('fields.actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items">
            <td :data-label="$t('fields.item')">
              <div class="indicator-box">
                <span class="indicator-label">
                  {{ item.name }}
                </span>
                <span :class="['indicator', borrowState(item)]"></span>
              </div>
            </td>
            <td :data-label="$t('fields.barcode')">{{ item.barcode }}</td>
            <td :data-label="$t('fields.required_qualifications')">
              <div class="tags">
                <span
                  v-for="qualification in item.required_qualifications"
                  class="tag">
                  {{ qualification.name }}
                </span>
              </div>
            </td>
            <td :data-label="$t('fields.actions')">
              <div class="buttons">
                <a :href="'/items/' + item.id + '/edit'" class="button is-primary is-small">
                  {{ $t('actions.edit') }}
                </a>
                <a :href="'/items/' + item.id" class="button is-small">
                  {{ $t('actions.view') }}
                </a>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <a href="/items/new" class="button">
        {{ $t('actions.create_item') }}
      </a>
    </div>`


export default {
    template,
    props: ['items', 'borrowstates'],
    methods: {
        isBorrowed: function(itemId) {
            return this.borrowstates.filter(
                bs => bs.borrowed_item.id === itemId && bs.returned_at === null
            ).length > 0;
        },
        borrowState: function(item) {
            return this.isBorrowed(item.id) ? 'borrowed' : 'available';
        },
    },
}
