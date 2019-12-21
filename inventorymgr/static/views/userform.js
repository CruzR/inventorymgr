const template = `
    <div>
    <div v-if="error" class="message is-danger">
      <div class="message-body">
        {{ error }}
      </div>
    </div>
    <form @submit.prevent="$emit('commit-user-change', user, repeatedPassword)">
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
      <template v-if="isEditContext && !changePassword">
        <div class="field">
          <label class="label">Password</label>
          <div class="control">
            <button
              type="button"
              class="button"
              @click="changePassword = true">
              Change password
            </button>
          </div>
        </div>
      </template>
      <template v-else-if="isCreateContext || (!isViewContext && changePassword)">
        <div class="field">
          <label class="label">New password</label>
          <div class="control">
            <input
              type="password"
              class="input"
              v-model="user.password">
          </div>
        </div>
        <div class="field">
          <label class="label">Repeat new password</label>
          <div class="control">
            <input
              type="password"
              class="input"
              v-model="repeatedPassword">
          </div>
        </div>
      </template>
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
      <div class="field is-grouped" v-else-if="isViewContext">
        <div class="control">
          <router-link
            :to="editUserUrl"
            v-slot="{ href, navigate }">
            <a class="button is-primary" :href="href" @click="navigate">
              Edit
            </a>
          </router-link>
        </div>
        <div class="control">
          <button type="button" class="button is-danger"
            @click="$emit('delete-user', current)">
            Delete
          </button>
        </div>
      </div>
    </form>
    </div>`

function editUserUrl() {
    if (this.current.id === this.$store.state.sessionUser.id) {
        return '/users/me/edit';
    }
    return '/users/' + this.current.id + '/edit';
}

export default {
    template,
    props: ['current', 'context', 'error'],
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
            changePassword: false,
            repeatedPassword: '',
        }
    },
    computed: {
        isViewContext: function() {
            return this.context === 'view';
        },
        isEditContext: function() {
            return this.context === 'edit';
        },
        isCreateContext: function() {
            return this.context === 'create';
        },
        editUserUrl
    }
}
