<template>
  <div class="input">
    <label v-if="!!this.$slots['default']" v-bind:for="id">
      <slot></slot>
    </label>
    <div v-bind:class="['field', { error: error }, { disabled: disabled }]">
      <div class="icon" v-if="icon">
        <i v-bind:class="icon"></i>
      </div>
      <input
        v-bind:type="password ? 'password' : 'text'"
        v-bind:id="id"
        v-bind:name="name"
        v-bind:placeholder="placeholder"
        v-bind:value="modelValue"
        ref="input"
        v-on:input="update_value"
        v-bind:disabled="disabled"
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
    modelValue: String,
    error: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['update:modelValue'],
  methods: {
    focus() {
      this.$refs.input.focus();
    },
    update_value(event) {
      // Update the local data
      this.value = event.target.value;

      // Send a event so the parent knows the value is changed
      this.$emit('update:modelValue', event.target.value);
    },
  },
};
</script>
