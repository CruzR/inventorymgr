const template = `
    <div>
    <div v-if="errorMessage" class="message is-danger">
      <div class="message-body">
        {{ errorMessage }}
      </div>
    </div>
    <form @submit.prevent="$emit('commit-user-change', user)">
      <div class="field">
        <label class="label">Username</label>
        <div class="control">
          <input
            type="text" placeholder="Username"
            :readonly="isViewContext"
            :class="{ 'input': true, 'is-static': isViewContext }"
            v-model="user.username">
        </div>
      </div>
      <div v-if="!isViewContext" class="field">
        <label class="label">Password</label>
        <div class="control">
          <input
            type="password" placeholder="Password"
            class="input"
            v-model="user.password">
        </div>
      </div>
      <fieldset class="field">
        <legend class="label">Permissions</legend>
        <div class="field">
          <label class="checkbox">
            <input
              type="checkbox"
              :disabled="isViewContext"
              v-model="user.create_users">
            Create Users
          </label>
        </div>
        <div class="field">
          <label class="checkbox">
            <input
              type="checkbox"
              :disabled="isViewContext"
              v-model="user.view_users">
            View Users
          </label>
        </div>
        <div class="field">
          <label class="checkbox">
            <input
              type="checkbox"
              :disabled="isViewContext"
              v-model="user.update_users">
            Update Users
          </label>
        </div>
        <div class="field">
          <label class="checkbox">
            <input
              type="checkbox"
              :disabled="isViewContext"
              v-model="user.edit_qualifications">
            Edit Qualifications
          </label>
        </div>
      </fieldset>
      <div class="field">
        <label class="label">Qualifications</label>
        <div class="control">
          <input
            type="text" placeholder="Qualifications"
            :readonly="isViewContext"
            :class="{ 'input': true, 'is-static': isViewContext }">
        </div>
      </div>
      <div class="field" v-if="context == 'create'">
        <div class="control">
          <button class="button is-primary" type="submit">Create</button>
        </div>
      </div>
      <div class="field is-grouped" v-else-if="context == 'edit'">
        <div class="control">
          <button class="button is-primary" type="submit">Save</button>
        </div>
        <div class="control">
          <button
            class="button" type="button"
            @click="$emit('cancel-user-change')">
            Cancel
          </button>
        </div>
      </div>
      <div class="field" v-else-if="isViewContext">
        <div class="control">
          <router-link
            :to="'/users/' + current.id + '/edit'"
            v-slots="{ href, navigate }">
            <a class="button is-primary" :href="href" @click="navigate">
              Edit
            </a>
          </router-link>
        </div>
      </div>
    </form>
    </div>`

export default {
    template,
    props: ['current', 'context'],
    data: function() {
        const user = (typeof(this.current) !== 'undefined')
            ? JSON.parse(JSON.stringify(this.current))
            : {
                username: '',
                password: '',
                create_users: false,
                view_users: false,
                update_users: false,
                edit_qualifications: false,
                qualifications: []
            };

        return {
            user,
            errorMessage: ''
        }
    },
    computed: {
        isViewContext: function() {
            return this.context === 'view';
        }
    }
}
