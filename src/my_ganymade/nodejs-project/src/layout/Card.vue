<template>
  <div class="card">
    <CardTitle>
      <slot name="title"></slot>
      <template #actions v-if="!!this.$slots['title_actions']">
        <slot name="title_actions"></slot>
      </template>
    </CardTitle>
    <div class="content" v-if="!!this.$slots['default']">
      <slot></slot>
    </div>
    <div class="actions">
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script>
import CardTitle from './CardTitle.vue';

export default {
  name: 'Card',
  components: {
    CardTitle,
  },
};
</script>
