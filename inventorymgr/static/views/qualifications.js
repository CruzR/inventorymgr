const template = `
    <table class="table">
      <thead>
        <tr>
          <th>Name</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="qualification in $store.state.qualifications">
          <td>{{ qualification.name }}</td>
        </tr>
      </tbody>
    </table>`

export default {
    template
}
