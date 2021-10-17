<template>
  <div class="header">
    <MenuToggle></MenuToggle>
    <Spacer></Spacer>
    <UserMenu></UserMenu>
  </div>
</template>

<script>
import MenuToggle from '../components/MenuToggle.vue';
import Spacer from '../components/Spacer.vue';
import UserMenu from '../components/UserMenu.vue';

export default {
  name: 'Header',
  components: { MenuToggle, Spacer, UserMenu },
};
</script>
