<template>
  <Flexbox centerv centerh id="app_loginform">
    <form v-on:submit="submit_form">
      <Card title_icon="fas fa-user-circle" v-bind:content_class="card_class">
        <template #title>Login</template>
        <template #title_actions>
          <CardTitleAction v-on:click="next_theme">
            <i class="fas fa-adjust"></i>
          </CardTitleAction>
        </template>

        <div>
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
        </div>

        <div>
          <Input
            id="second_factor"
            ref="second_factor"
            icon="fas fa-user"
            placeholder="Second factor"
            v-model="username"
            v-bind:disabled="loading"
          >
            Two factor authentication code
          </Input>
        </div>

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
      state: 'credentials',
    };
  },
  computed: {
    card_class: function () {
      // Computed data to calculate the value for the classname of the
      // content DIV for the Card.
      let card_class = 'pages';
      if (this.state == 'second_factor') {
        card_class += ' show_second_factor';
      }
      return card_class;
    },
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

      // TODO: Validate the given data

      // TODO: Validate credentials with backend

      // TODO: If the backend tells us to retrieve the second factor,
      //       redirect the user to the second factor. We can do this
      //       by setting the 'state' to 'second_factor'.
      // this.state = 'second_factor';

      // TODO: If the backend tells us the credentials are corret, we
      //       redirect the user to the correct URL.

      // TODO: If the backend tells us the credentials were not corret,
      //       we abort and set every INPUT to error.

      // Send the command to login
      console.log(this.username);
      console.log(this.password);
    },
  },
};
</script>
