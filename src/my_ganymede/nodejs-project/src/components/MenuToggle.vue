<template>
  <div class="menutoggle">
    <i
      class="fas fa-bars"
      v-on:click="toggle_menu"
      v-bind:class="{ hidden: !nav_is_visible }"
    ></i>
  </div>
</template>

<script>
export default {
  name: 'MenuToggle',
  computed: {
    nav_is_visible() {
      return this.$store.state.ui.navigation_visible;
    },
  },
  methods: {
    toggle_menu() {
      this.$store.commit('navigation_visible_toggle');
    },
  },
};
</script>
