<template>
  <div class="title">
    <div class="icon" v-if="icon">
      <i v-bind:class="icon"></i>
    </div>
    <div class="text">
      <slot></slot>
    </div>
    <div class="actions" v-if="!!$slots.actions">
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CardTitle',
  props: {
    icon: String,
  },
};
</script>