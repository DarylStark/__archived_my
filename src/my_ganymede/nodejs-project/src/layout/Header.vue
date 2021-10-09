<template>
  <div class="header">
    <MenuToggle></MenuToggle>
  </div>
</template>

<script>
import MenuToggle from '../components/MenuToggle.vue';

export default {
  name: 'Header',
  components: { MenuToggle },
};
</script>
