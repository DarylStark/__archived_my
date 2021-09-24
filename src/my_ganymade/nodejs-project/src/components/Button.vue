<template>
  <button class="button">
    <div>
      <div class="icon" v-if="!!this.$slots['icon']">
        <slot name="icon"></slot>
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
};
</script>
