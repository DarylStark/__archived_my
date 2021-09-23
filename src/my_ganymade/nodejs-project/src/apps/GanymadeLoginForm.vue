<template>
  <div id="app_loginform">
    <Card>
      <template #title>Login</template>
      <template #title_actions>
        <CardTitleAction v-on:click="next_theme">
          <i class="fas fa-adjust"></i>
        </CardTitleAction>
      </template>
    </Card>
  </div>
</template>

<script>
import UI from '../mgm/ui';
import Card from '../layout/Card.vue';
import CardTitleAction from '../layout/CardTitleAction.vue';

export default {
  name: 'GanymadeLogin',
  components: {
    Card,
    CardTitleAction,
  },
  data: () => {
    return {
      theme_index: UI.get_current_theme_index(),
    };
  },
  methods: {
    next_theme: function () {
      // Set the next theme
      UI.next_theme();

      // Update the index
      this.theme_index = UI.get_current_theme_index();
    },
  },
};
</script>
