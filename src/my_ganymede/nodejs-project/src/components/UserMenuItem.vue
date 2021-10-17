<template>
  <div class="item">
    <div class="icon" v-if="icon">
      <i v-bind:class="['fas', icon]"></i>
    </div>
    <div class="text">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserMenuItem',
  props: {
    icon: String,
  },
};
</script>
