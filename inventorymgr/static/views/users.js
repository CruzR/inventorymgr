const template = `
    <table class="table is-fullwidth responsive-table">
      <thead>
        <tr>
          <th>Username</th>
          <th><abbr title="Create Users">CU</abbr></th>
          <th><abbr title="View Users">VU</abbr></th>
          <th><abbr title="Update Users">UU</abbr></th>
          <th><abbr title="Edit Qualifications">EQ</abbr></th>
          <th>Qualifications</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in $store.state.users">
          <td data-label="Username">{{ user.username }}</td>
          <td data-label="Create Users"><input type="checkbox" :checked="user.create_users" disabled></td>
          <td data-label="View Users"><input type="checkbox" :checked="user.view_users" disabled></td>
          <td data-label="Update Users"><input type="checkbox" :checked="user.update_users" disabled></td>
          <td data-label="Edit Qualifications"><input type="checkbox" :checked="user.edit_qualifications" disabled></td>
          <td data-label="Qualifications"><span>{{ user.qualifications.map(q => q.name).join(", ") }}</span></td>
          <td data-label="Actions">
            <div class="control">
              <router-link
                :to="'/users/' + user.id + '/edit'"
                v-slot="{ href, navigate }">
                <a class="button is-primary is-small" :href="href" @click="navigate">
                  Edit
                </a>
              </router-link>
              <router-link
                :to="'/users/' + user.id"
                v-slot="{ href, navigate }">
                <a class="button is-primary is-small" :href="href" @click="navigate">
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
