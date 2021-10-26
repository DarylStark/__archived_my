<template>
  <div v-bind:class="['navigation', { hide: !visible }]">
    Navigation: {{ visible }}
  </div>
</template>

<script>
export default {
  name: 'Navigation',
  computed: {
    visible() {
      return this.$store.state.ui.navigation_visible;
    },
  },
};
</script>
