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
            v-bind:error="invalid_username"
            validate_re="^[A-Za-z0-9_\.\-]+$"
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
            v-bind:error="invalid_password"
            validate_re="^.+$"
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
            v-model="second_factor"
            v-bind:disabled="loading"
            validate_re="^\d{6}$"
            v-bind:error="invalid_second_factor"
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
import axios from 'axios';

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
      second_factor: '',
      invalid_username: false,
      invalid_password: false,
      invalid_second_factor: false,
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

      this.invalid_username = !this.$refs.username.is_valid();
      this.invalid_password = !this.$refs.password.is_valid();
      this.invalid_second_factor = !this.$refs.second_factor.is_valid();

      // Set state to loading
      this.loading = true;

      // Set a new 'this' to use in the callbacks for Axios
      let vue_this = this;

      // Validate the given data
      let valid = false;
      if (this.state == 'credentials') {
        valid =
          this.$refs.username.is_valid() && this.$refs.password.is_valid();
      } else {
        valid = this.$refs.second_factor.is_valid();
      }

      // Create a data object to send to the backend
      let second_factor = this.second_factor === '' ? null : this.second_factor;

      let data_object = {
        username: this.username,
        password: this.password,
        second_factor: second_factor,
      };

      // Validate credentials with backend
      if (valid) {
        axios
          .post('/data/aaa/login', data_object)
          .then((response) => {
            // We received data back
            let success = response.data.success;

            if (!success) {
              // The data indicated that the credentials were not
              // correct. We need to check what went wrong
              if (response.data.reason == 'second_factor_needed') {
                // We didn't specify any second factor but the backend
                // tells us we need them. Redirect user to 'second
                // factor' page
                vue_this.invalid_second_factor = false;
                vue_this.second_factor = '';
                vue_this.state = 'second_factor';

                // TODO: Focus the 'second_factor' field. Harder then
                //       you think.
              } else {
                // Credentials are wrong. Make sure the user is on the
                // credentials page and set the 'invalid_' fields to
                // true.
                vue_this.state = 'credentials';
                vue_this.password = '';
                vue_this.second_factor = '';
                vue_this.invalid_username = true;
                vue_this.invalid_password = true;

                // TODO: Focus the 'usernamae' field. Harder then you
                //       think.
              }

              // Done, stop the loading
              vue_this.loading = false;
            } else {
              // TODO: Redirect the user to the dashboardpage
              console.log('Logged in!');
            }
          })
          .catch((error) => {
            // TODO: display error (toast?)
            console.error('ERROR: ' + error);

            // Done with the request, not loading anymore :-)
            vue_this.loading = false;
          });
      } else {
        this.loading = false;
        this.$refs.username.focus(true);
      }
    },
  },
};
</script>
