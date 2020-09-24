import { updateUser } from '/static/api.js'
import UserForm from '/static/views/userform.js'


const template = `
    <user-form
      v-if="currentUser"
      :current="currentUser"
      :sessionUser="sessionUser"
      :qualifications="qualifications"
      :error="errorMessage"
      context="edit"
      @commit-user-change="sendUpdateUserRequest"
      @cancel-user-change="returnToUsers">
    </user-form>`

function sendUpdateUserRequest(user, repeatedPassword) {
    if ((user.password || repeatedPassword) && user.password !== repeatedPassword) {
        this.errorMessage = this.$t('errors.password_mismatch');
        return;
    }

    if (!user.password) {
        delete user.password;
    }

    updateUser(this.userId, user).then(response => {
        if (response.success) {
            location = location.origin + '/users';
        } else {
            console.error(response.error);
            this.errorMessage = this.$t(`errors.${response.error.reason}`);
        }
    })
}

function returnToUsers() {
    location = location.origin + '/users/' + this.userId;
}

export default {
    template,
    props: ['sessionUser', 'qualifications', 'users'],
    data: () => {
        return { errorMessage: '' }
    },
    computed: {
        userId: function() {
            const path = location.pathname.split('/');
            const idComponent = path[path.length - 2];
            return (idComponent === 'me') ? idComponent : parseInt(idComponent);
        },
        currentUser: function() {
            if (this.userId === 'me') {
                return this.sessionUser;
            }
            const id = this.userId;
            return this.users.find(u => u.id === id);
        },
    },
    methods: {
        sendUpdateUserRequest,
        returnToUsers
    },
    components: {
        UserForm
    }
}
