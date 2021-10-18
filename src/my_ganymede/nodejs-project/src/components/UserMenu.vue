<template>
  <div class="usermenu">
    <div class="button">
      <div v-if="user_fullname">{{ user_fullname }}</div>
      <i class="fas fa-user-circle"></i>
    </div>
    <div class="menu">
      <UserMenuItem icon="fa-cog">Settings</UserMenuItem>
      <UserMenuItem icon="fa-adjust" v-on:click="next_theme"
        >Next theme</UserMenuItem
      >
      <UserMenuItem icon="fa-edit">Rename session</UserMenuItem>
      <UserMenuItem icon="fa-sign-out-alt" v-on:click="logout"
        >Logout</UserMenuItem
      >
    </div>
  </div>
</template>

<script>
import Ganymede from '../mgm/ganymede.js';
import UserMenuItem from './UserMenuItem.vue';

export default {
  name: 'UserMenu',
  components: { UserMenuItem },
  computed: {
    user_fullname() {
      return this.$store.state.session.account.fullname;
    },
  },
  methods: {
    next_theme: () => {
      Ganymede.commands.execute('theme.next');
    },
    logout: () => {
      Ganymede.commands.execute('userssion.logout');
    },
  },
};
</script>
