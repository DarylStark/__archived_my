<template>
  <Flexbox centerv centerh id="app_loginform">
    <Card title_icon="fas fa-adjust">
      <template #title>Login</template>
      <template #title_actions>
        <CardTitleAction v-on:click="next_theme">
          <i class="fas fa-adjust"></i>
        </CardTitleAction>
      </template>
      <Input
        id="username"
        ref="username"
        icon="fas fa-user"
        placeholder="Username"
      >
        Username
      </Input>
      <Input
        id="password"
        password
        ref="password"
        icon="fas fa-key"
        placeholder="Password"
      >
        Password
      </Input>
      <template #actions>
        <Button>Login</Button>
      </template>
    </Card>
  </Flexbox>
</template>

<script>
import UI from '../mgm/ui';
import Flexbox from '../layout/Flexbox';
import Card from '../layout/Card.vue';
import CardTitleAction from '../layout/CardTitleAction.vue';
import Input from '../components/Input.vue';
import Button from '../components/Button.vue';

export default {
  name: 'GanymadeLogin',
  components: {
    Flexbox,
    Card,
    CardTitleAction,
    Input,
    Button,
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
