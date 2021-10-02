<template>
  <div v-bind:class="['flexbox', { 'center-v': centerv, 'center-h': centerh }]">
    <slot></slot>
  </div>
</template>

<script>
import CardTitle from './CardTitle.vue';

export default {
  name: 'Flexbox',
  props: {
    centerv: Boolean,
    centerh: Boolean,
  },
};
</script>
