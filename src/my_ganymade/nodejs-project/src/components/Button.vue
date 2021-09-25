<template>
  <button class="button" v-bind:type="type" v-bind:disabled="!is_enabled">
    <div>
      <div class="icon" v-if="icon">
        <i v-bind:class="icon"></i>
      </div>
      <div class="text" v-if="!!this.$slots['default']">
        <slot></slot>
      </div>
    </div>
  </button>
</template>

<script>
export default {
  name: 'Button',
  props: {
    icon: String,
    type: {
      type: String,
      default: 'button',
    },
    enabled: {
      type: Boolean,
      default: true,
    },
  },
  data: function () {
    return {
      is_enabled: true,
    };
  },
  mounted() {
    // Set the properties to data values
    this.is_enabled = this.enabled;
  },
  methods: {
    set_enabled(enabled) {
      this.is_enabled = enabled;
    },
  },
};
</script>
