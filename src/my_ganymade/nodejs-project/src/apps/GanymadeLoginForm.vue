<template>
  <Flexbox centerv centerh id="app_loginform">
    <form v-on:submit="submit_form">
      <Card title_icon="fas fa-user-circle">
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
          v-model="username"
          v-bind:disabled="loading"
        >
          Username
        </Input>
        <Input
          id="password"
          password
          ref="password"
          icon="fas fa-key"
          placeholder="Password"
          v-model="password"
          v-bind:disabled="loading"
        >
          Password
        </Input>
        <template #actions>
          <Button
            icon="fas fa-sign-in-alt"
            type="submit"
            ref="submit"
            v-bind:loading="loading"
            v-bind:disabled="loading"
          >
            Login
          </Button>
        </template>
      </Card>
    </form>
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
      username: '',
      password: '',
      loading: false,
    };
  },
  methods: {
    next_theme() {
      // Set the next theme
      UI.next_theme();

      // Update the index
      this.theme_index = UI.get_current_theme_index();
    },
    submit_form(event) {
      // Prevent the default handler
      event.preventDefault();

      // Set state to loading
      this.loading = true;

      // Send the command to login
      console.log(this.username);
      console.log(this.password);
    },
  },
};
</script>
