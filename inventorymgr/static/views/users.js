const template = `
    <table class="table">
      <thead>
        <tr>
          <th>Username</th>
          <th><abbr title="Create Users">CU</abbr></th>
          <th><abbr title="View Users">VU</abbr></th>
          <th><abbr title="Update Users">UU</abbr></th>
          <th><abbr title="Edit Qualifications">EQ</abbr></th>
          <th>Qualifications</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in $store.state.users">
          <td>{{ user.username }}</td>
          <td><input type="checkbox" :checked="user.create_users" disabled></td>
          <td><input type="checkbox" :checked="user.view_users" disabled></td>
          <td><input type="checkbox" :checked="user.update_users" disabled></td>
          <td><input type="checkbox" :checked="user.edit_qualifications" disabled></td>
          <td>{{ user.qualifications.map(q => q.name).join(", ") }}</td>
          <th>
            <div class="control">
              <router-link
                :to="'/users/' + user.id + '/edit'"
                v-slots="{ href, navigate }">
                <a class="button is-primary is-small" :href="href" @click="navigate">
                  Edit
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
