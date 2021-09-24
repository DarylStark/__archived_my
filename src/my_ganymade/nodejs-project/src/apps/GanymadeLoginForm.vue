<template>
  <Flexbox centerv centerh id="app_loginform">
    <Card>
      <template #title>Login</template>
      <template #title_actions>
        <CardTitleAction v-on:click="next_theme">
          <i class="fas fa-adjust"></i>
        </CardTitleAction>
      </template>
      <Input id="username" ref="username" icon="fas fa-user">Username</Input>
      <Input id="password" password ref="password" icon="fas fa-key"
        >Password</Input
      >
    </Card>
  </Flexbox>
</template>

<script>
import UI from '../mgm/ui';
import Flexbox from '../layout/Flexbox';
import Card from '../layout/Card.vue';
import CardTitleAction from '../layout/CardTitleAction.vue';
import Input from '../components/Input.vue';

export default {
  name: 'GanymadeLogin',
  components: {
    Flexbox,
    Card,
    CardTitleAction,
    Input,
  },
  mounted() {
    this.$refs.username.focus();
  },
  data: () => {
    return {
      theme_index: UI.get_current_theme_index(),
    };
  },
  methods: {
    next_theme() {
      // Set the next theme
      UI.next_theme();

      // Update the index
      this.theme_index = UI.get_current_theme_index();
    },
  },
};
</script>
