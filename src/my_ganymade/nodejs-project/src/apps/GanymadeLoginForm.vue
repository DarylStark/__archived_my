<template>
  <div id="app_loginform">
    <Input value="username"></Input>
    <Input value="password"></Input>
  </div>
</template>

<script>
import Input from "../components/Input.vue";

export default {
  name: "GanymadeLogin",
  components: {
    Input,
  },
};
</script>
