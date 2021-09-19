<template>
  <input v-bind:value="value" />
</template>

<script>
export default {
  name: "Input",
  props: ["value"],
};
</script>
