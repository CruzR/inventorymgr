const template = `
    <div>
      <table class="table is-fullwidth responsive-table">
        <thead>
          <tr>
            <th>{{ $t('fields.qualification') }}</th>
            <th>{{ $t('fields.actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="qualification in qualifications">
            <td :data-label="$t('fields.qualification')">{{ qualification.name }}</td>
            <td :data-label="$t('fields.actions')">
              <div class="buttons">
                <a :href="'/qualifications/' + qualification.id + '/edit'" class="button is-primary is-small">
                  {{ $t('actions.edit') }}
                </a>
                <a :href="'/qualifications/' + qualification.id" class="button is-small">
                  {{ $t('actions.view') }}
                </a>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <a href="/qualifications/new" class="button">
        {{ $t('actions.create_qualification') }}
      </a>
    </div>
    `


export default {
    template,
    props: ['qualifications'],
}
