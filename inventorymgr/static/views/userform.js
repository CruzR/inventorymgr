import { mapState } from '/static/vuex.esm.browser.js'
import TagSelectBox from '/static/views/tagselectbox.js'

const template = `
    <div>
    <div v-if="error" class="message is-danger">
      <div class="message-body">
        {{ error }}
      </div>
    </div>
    <form @submit.prevent="$emit('commit-user-change', user, repeatedPassword)">
      <div class="field">
        <label class="label" for="userform-username">{{ $t('fields.username') }}</label>
        <div class="control">
          <input
            id="userform-username"
            type="text" required
            :readonly="isViewContext"
            :class="{ 'input': true, 'is-static': isViewContext }"
            v-model="user.username">
        </div>
      </div>
      <div v-if="!isCreateContext" class="field">
        <label class="label" for="userform-barcode">{{ $t('fields.barcode') }}</label>
        <div class="control">
          <input
            id="userform-barcode"
            type="text" readonly
            class="input is-static"
            :value="user.barcode">
        </div>
      </div>
      <template v-if="isEditContext && !changePassword">
        <div class="field">
          <label class="label">{{ $t('fields.password') }}</label>
          <div class="control">
            <button
              type="button"
              class="button"
              @click="changePassword = true">
              {{ $t('actions.change_password') }}
            </button>
          </div>
        </div>
      </template>
      <template v-else-if="isCreateContext || (!isViewContext && changePassword)">
        <div class="field">
          <label class="label" for="userform-password">{{ $t('fields.new_password') }}</label>
          <div class="control">
            <input
              id="userform-password"
              type="password"
              class="input"
              v-model="user.password">
          </div>
        </div>
        <div class="field">
          <label
            class="label"
            for="userform-repeatpassword">{{ $t('fields.repeat_new_password') }}</label>
          <div class="control">
            <input
              id="userform-repeatpassword"
              type="password"
              class="input"
              v-model="repeatedPassword">
          </div>
        </div>
      </template>
      <fieldset class="field">
        <legend class="label">{{ $t('fields.permissions') }}</legend>
        <div class="field">
          <label class="checkbox">
            <input
              type="checkbox"
              :disabled="isViewContext"
              v-model="user.create_users">
            {{ $t('permissions.create_users') }}
          </label>
        </div>
        <div class="field">
          <label class="checkbox">
            <input
              type="checkbox"
              :disabled="isViewContext"
              v-model="user.view_users">
            {{ $t('permissions.view_users') }}
          </label>
        </div>
        <div class="field">
          <label class="checkbox">
            <input
              type="checkbox"
              :disabled="isViewContext"
              v-model="user.update_users">
            {{ $t('permissions.update_users') }}
          </label>
        </div>
        <div class="field">
          <label class="checkbox">
            <input
              type="checkbox"
              :disabled="isViewContext"
              v-model="user.edit_qualifications">
            {{ $t('permissions.edit_qualifications') }}
          </label>
        </div>
        <div class="field">
          <label class="checkbox">
            <input
              type="checkbox"
              :disabled="isViewContext"
              v-model="user.create_items">
            {{ $t('permissions.create_items') }}
          </label>
        </div>
        <div class="field">
          <label class="checkbox">
            <input
              type="checkbox"
              :disabled="isViewContext"
              v-model="user.manage_checkouts">
            {{ $t('permissions.manage_checkouts') }}
          </label>
        </div>
      </fieldset>
      <div class="field">
        <label class="label">{{ $t('fields.qualifications') }}</label>
        <div class="control">
          <tag-select-box
            :items.sync="user.qualifications"
            :readonly="isViewContext"
            :choices="qualifications">
          </tag-select-box>
        </div>
      </div>
      <div class="field" v-if="context == 'create'">
        <div class="control">
          <button class="button is-primary" type="submit">{{ $t('actions.create') }}</button>
        </div>
      </div>
      <div class="field is-grouped" v-else-if="context == 'edit'">
        <div class="control">
          <button class="button is-primary" type="submit">{{ $t('actions.save') }}</button>
        </div>
        <div class="control">
          <button
            class="button" type="button"
            @click="$emit('cancel-user-change')">
            {{ $t('actions.cancel') }}
          </button>
        </div>
      </div>
      <div class="field is-grouped" v-else-if="isViewContext">
        <div class="control">
          <router-link
            :to="editUserUrl"
            v-slot="{ href, navigate }">
            <a class="button is-primary" :href="href" @click="navigate">
             {{ $t('actions.edit') }}
            </a>
          </router-link>
        </div>
        <div class="control">
          <button type="button" class="button is-danger"
            @click="$emit('delete-user', current)">
            {{ $t('actions.delete') }}
          </button>
        </div>
      </div>
    </form>
    </div>`

function editUserUrl() {
    if (this.current.id === this.sessionUser.id) {
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
                create_items: false,
                manage_checkouts: false,
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
        editUserUrl,
        ...mapState(['qualifications', 'sessionUser']),
    },
    components: { TagSelectBox }
}
