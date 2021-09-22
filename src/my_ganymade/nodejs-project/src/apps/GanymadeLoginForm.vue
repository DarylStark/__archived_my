<template>
  <div id="app_loginform">
    <card title="Login">Loginform</card>
  </div>
</template>

<script>
import UI from "../mgm/ui";
import Card from "../layout/Card.vue";

export default {
  name: "GanymadeLogin",
  created: () => {
    UI.set_theme();
  },
  components: {
    Card,
  },
};
</script>
