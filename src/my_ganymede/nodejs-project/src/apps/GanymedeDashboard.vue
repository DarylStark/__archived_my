<template>
  <div id="dashboard">
    <Header></Header>
    <div class="content_nav">
      <Navigation></Navigation>
      <Content></Content>
    </div>
  </div>
</template>

<script>
import Header from '../layout/Header.vue';
import Navigation from '../layout/Navigation.vue';
import Content from '../layout/Content.vue';
import Ganymede from '../mgm/ganymede.js';
import APICommand from '../mgm/api_command';

export default {
  name: 'GanymedeDashboard',
  components: { Header, Navigation, Content },
  created: function () {
    // Set a local variable that the callsbacks can use for 'this'
    let cb_this = this;

    // Retrieve UserSession and User details
    Ganymede.api.execute(
      new APICommand(
        'user_sessions',
        'current',
        'GET',
        null,
        function (data) {
          // We have the details. Let's save the user account and the
          // session to the store for later user
          cb_this.$store.commit('set_session', data.data);
        },
        (error) => {
          // TODO: give error
          console.log(error);
        }
      )
    );
  },
};
</script>
