<template>
  <div class="card">
    <CardTitle v-if="title">{{ title }}</CardTitle>
    <div class="content">
      <slot></slot>
    </div>
  </div>
</template>

<script>
import CardTitle from './CardTitle.vue';

export default {
  name: 'Card',
  props: {
    title: String,
  },
  components: {
    CardTitle,
  },
};
</script>
