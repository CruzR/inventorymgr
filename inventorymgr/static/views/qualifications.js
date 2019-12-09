const template = `
    <table class="table">
      <thead>
        <tr>
          <th>Name</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="qualification in $store.state.qualifications">
          <td>{{ qualification.name }}</td>
          <td>
            <router-link
              :to="'/qualifications/' + qualification.id"
              v-slot="{ href, navigate }">
              <a :href="href" class="button is-primary is-small" @click="navigate">
                View
              </a>
            </router-link>
          </td>
        </tr>
      </tbody>
    </table>`

export default {
    template
}
