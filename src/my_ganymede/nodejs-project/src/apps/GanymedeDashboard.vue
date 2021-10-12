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
import Ganymede from '../mgm/ganymede';
import Header from '../layout/Header.vue';
import Navigation from '../layout/Navigation.vue';
import Content from '../layout/Content.vue';

export default {
  name: 'GanymedeDashboard',
  components: { Header, Navigation, Content },
};
</script>
