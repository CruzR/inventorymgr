const template = `
    <router-link :to="to" v-slot="{ href, navigate }">
      <a :href="href" :class="classes" @click="navigate">
        <slot></slot>
      </a>
    </router-link>
    `


export default {
    template,
    props: ['to', 'kind'],
    computed: {
        classes: function() {
            if (this.kind) {
                return ['button', this.kind.split()];
            }
            return ['button'];
        },
    },
}
