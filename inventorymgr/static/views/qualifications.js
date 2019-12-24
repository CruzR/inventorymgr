const template = `
    <table class="table is-fullwidth responsive-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="qualification in $store.state.qualifications">
          <td data-label="Name">{{ qualification.name }}</td>
          <td data-label="Actions">
            <div class="control">
              <router-link
                :to="'/qualifications/' + qualification.id + '/edit'"
                v-slot="{ href, navigate }">
                <a :href="href" class="button is-primary is-small" @click="navigate">
                  Edit
                </a>
              </router-link>
              <router-link
                :to="'/qualifications/' + qualification.id"
                v-slot="{ href, navigate }">
                <a :href="href" class="button is-primary is-small" @click="navigate">
                  View
                </a>
              </router-link>
            </div>
          </td>
        </tr>
      </tbody>
    </table>`

export default {
    template
}
