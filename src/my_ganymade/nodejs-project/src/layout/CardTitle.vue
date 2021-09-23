<template>
  <div class="title">
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
};
</script>