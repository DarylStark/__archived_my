<template>
  <div class="card">
    <div v-if="title">{{ title }}</div>
    <div>Card content comes here</div>
  </div>
</template>

<script>
export default {
  name: "Card",
  props: {
    title: String,
  },
};
</script>