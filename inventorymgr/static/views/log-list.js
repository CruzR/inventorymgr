const template = `
    <ul>
      <li v-for="logentry in logsWithKnownType">
        {{ logentry.timestamp }}:
        {{ $t('messages.logs.' + logentry.action, formatLog(logentry)) }}
      </li>
    </ul>
    `


function itemById(item_id) {
    return this.items.find(i => i.id === item_id);
}

function userById(user_id) {
    return this.users.find(u => u.id === user_id);
}


export default {
    template,
    props: ['logs', 'items', 'users'],
    computed: {
        logsWithKnownType: function() {
            let filteredLogs = this.logs.filter(
                l => ['checkout', 'checkin', 'transfer'].some(a => a === l.action)
            );
            filteredLogs.sort((a, b) => {
                if (a.timestamp > b.timestamp) return -1;
                if (a.timestamp < b.timestamp) return 1;
                return 0;
            });
            return filteredLogs;
        },
    },
    methods: {
        formatLog: function(logentry) {
            const secondary = this.userById(logentry.secondary_id);
            const secondary_name = secondary ? secondary.username : '';
            return {
                subject: this.userById(logentry.subject_id).username,
                items: logentry.items.map(i => this.itemById(i.id).name).join(', '),
                secondary: secondary_name,
            };
        },
        itemById,
        userById,
    },
}
