import { mapGetters } from '/static/vuex.esm.browser.js'


const template = `
    <ul>
      <li v-for="logentry in logsWithKnownType">
        {{ logentry.timestamp }}:
        {{ $t('messages.logs.' + logentry.action, formatLog(logentry)) }}
      </li>
    </ul>
    `


export default {
    template,
    props: ['logs'],
    computed: {
        logsWithKnownType: function() {
            let filteredLogs = this.logs.filter(l => l.action === 'checkout');
            filteredLogs.sort((a, b) => {
                if (a.timestamp > b.timestamp) return -1;
                if (a.timestamp < b.timestamp) return 1;
                return 0;
            });
            return filteredLogs;
        },
        ...mapGetters(['itemById', 'userById']),
    },
    methods: {
        formatLog: function(logentry) {
            return {
                subject: this.userById(logentry.subject_id).username,
                items: logentry.items.map(i => this.itemById(i.id).name).join(', '),
            };
        },
    },
}
