<template>
  <div id="app_loginform">
    <Input value="username"></Input>
    <Input value="password"></Input>
    <p>Random text</p>
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
