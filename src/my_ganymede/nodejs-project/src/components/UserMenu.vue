<template>
  <div class="usermenu">
    <div class="button">
      <div
        v-if="
          $store.state.user_session.session.account.fullname &&
          $store.state.ui.device_type != 'phone'
        "
      >
        {{ $store.state.user_session.session.account.fullname }}
      </div>
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
