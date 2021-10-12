<template>
  <div class="header">
    <MenuToggle></MenuToggle>
    <Spacer></Spacer>
  </div>
</template>

<script>
import MenuToggle from '../components/MenuToggle.vue';
import Spacer from '../components/Spacer.vue';

export default {
  name: 'Header',
  components: { MenuToggle, Spacer },
};
</script>
