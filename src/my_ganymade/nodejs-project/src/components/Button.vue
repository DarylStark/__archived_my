<template>
  <button class="button">
    <div>
      <div class="icon" v-if="icon">
        <i v-bind:class="icon"></i>
      </div>
      <div class="text" v-if="!!this.$slots['default']">
        <slot></slot>
      </div>
    </div>
  </button>
</template>

<script>
export default {
  name: 'Button',
  props: {
    icon: String,
  },
};
</script>
