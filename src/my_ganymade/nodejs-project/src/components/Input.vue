<template>
  <div class="input">
    <label v-if="!!this.$slots['default']" v-bind:for="id">
      <slot></slot>
    </label>
    <input
      v-bind:type="password ? 'password' : 'text'"
      v-bind:id="id"
      v-bind:name="name"
      ref="input"
    />
  </div>
</template>

<script>
export default {
  name: 'Input',
  props: {
    id: {
      type: String,
      required: true,
    },
    name: String,
    password: Boolean,
  },
  methods: {
    focus() {
      this.$refs.input.focus();
    },
  },
};
</script>
