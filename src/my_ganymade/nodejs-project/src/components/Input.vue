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
  },
  data: function () {
    return {
      is_error: false,
    };
  },
  emits: ['update:modelValue'],
  mounted() {
    // Set the error value
    this.is_error = this.error;
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
  },
};
</script>
