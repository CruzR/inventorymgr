const template = `
    <div>
      <table class="table is-fullwidth responsive-table">
        <thead>
          <tr>
            <th>Item</th>
            <th>Barcode</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in $store.state.items">
            <td data-label="Item">{{ item.name }}</td>
            <td data-label="Barcode">{{ item.barcode }}</td>
            <td data-label="Actions">
              <div class="field is-grouped">
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>`


export default {
  template,
}
