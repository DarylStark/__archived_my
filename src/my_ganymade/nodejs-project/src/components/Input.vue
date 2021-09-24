<template>
  <div class="input">
    <label v-if="!!this.$slots['default']" v-bind:for="id">
      <slot></slot>
    </label>
    <div class="field">
      <div class="icon" v-if="icon">
        <i v-bind:class="icon"></i>
      </div>
      <input
        v-bind:type="password ? 'password' : 'text'"
        v-bind:id="id"
        v-bind:name="name"
        v-bind:placeholder="placeholder"
        ref="input"
      />
    </div>
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
    icon: String,
    placeholder: String,
  },
  methods: {
    focus() {
      this.$refs.input.focus();
    },
  },
};
</script>
