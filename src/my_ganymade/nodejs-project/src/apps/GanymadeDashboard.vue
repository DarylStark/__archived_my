<template>
  <div>
    <p>Dashboard will be here</p>
  </div>
</template>

<script>
import UI from "../mgm/ui";

export default {
  name: "GanymadeDashboard",
  created: function () {
    UI.set_theme();
  },
};
</script>
