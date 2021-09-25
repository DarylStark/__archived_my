<template>
  <div class="input">
    <label v-if="!!this.$slots['default']" v-bind:for="id">
      <slot></slot>
    </label>
    <div v-bind:class="['field', { error: is_error }]">
      <div class="icon" v-if="icon">
        <i v-bind:class="icon"></i>
      </div>
      <input
        v-bind:type="password ? 'password' : 'text'"
        v-bind:id="id"
        v-bind:name="name"
        v-bind:placeholder="placeholder"
        v-bind:value="value"
        ref="input"
        v-on:input="update_value"
        v-bind:disabled="!is_enabled"
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
    enabled: {
      type: Boolean,
      default: true,
    },
  },
  data: function () {
    return {
      is_error: false,
      is_enabled: true,
    };
  },
  emits: ['update:modelValue'],
  mounted() {
    // Set the properties to data values
    this.is_error = this.error;
    this.is_enabled = this.enabled;
  },
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
    set_error(error) {
      this.is_error = error;
    },
    set_enabled(enabled) {
      this.is_enabled = enabled;
    },
  },
};
</script>
