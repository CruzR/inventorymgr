import { deleteUser, logout } from '/static/api.js'
import DeleteDialog from '/static/views/delete-dialog.js'
import UserForm from '/static/views/userform.js'

const template = `
    <div>
      <delete-dialog
        :show="showDeleteWarning"
        @cancel-delete="showDeleteWarning=false"
        @commit-delete="sendDeleteUserRequest(currentUser)">
        {{ $t('messages.delete_user', {name: currentUser.username}) }}
      </delete-dialog>
      <user-form
        v-if="currentUser"
        :current="currentUser"
        :session-user="sessionUser"
        :qualifications="qualifications"
        context="view"
        @delete-user="showDeleteWarning=true">
      </user-form>
    </div>
    `

function idFromUrl() {
    const path = location.pathname.split("/");
    const idComponent = path[path.length - 1];
    if (idComponent === 'me') {
        return idComponent;
    }
    return parseInt(idComponent);
}

function currentUser() {
    const id = idFromUrl();
    if (id === 'me') {
        return this.sessionUser;
    }
    return this.users.find(u => u.id === id);
}

function sendDeleteUserRequest(user) {
    const id = idFromUrl();
    deleteUser(id).then(response => {
        if (response.success) {
            if (id === 'me') {
                logout().then(response => {
                    location = location.origin + '/login';
                })
            } else {
                location = location.origin + '/users';
            }
        } else {
            console.error(response.error);
            this.errorMessage = this.$t(`errors.${response.error.reason}`);
        }
    })
}

export default {
    template,
    data: () => { return { showDeleteWarning: false }; },
    props: ['sessionUser', 'qualifications', 'users'],
    computed: {
        currentUser,
    },
    methods: {
        sendDeleteUserRequest
    },
    components: {
        UserForm,
        DeleteDialog,
    }
}
