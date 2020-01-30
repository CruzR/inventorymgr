const template = `
    <div :class="{ modal: true, 'is-active': show }">
      <div class="modal-background"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">{{ $t('actions.delete') }}</p>
          <button
            class="delete" aria-label="close" @click="$emit('cancel-delete')"></button>
        </header>
        <section class="modal-card-body">
          <slot></slot>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-danger" @click="$emit('commit-delete')">
            {{ $t('actions.delete') }}
          </button>
          <button class="button" @click="$emit('cancel-delete')">
            {{ $t('actions.cancel') }}
          </button>
        </footer>
      </div>
    </div>
    `


export default {
    template,
    props: ['show'],
}
