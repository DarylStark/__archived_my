<template>
  <div>
    <p>Dashboard will be here</p>
  </div>
</template>

<script>
import MGM from "../my_ganymade";

export default {
  name: "GanymadeDashboard",
  created: function () {
    MGM.set_colorscheme("dark");
  },
};
</script>
