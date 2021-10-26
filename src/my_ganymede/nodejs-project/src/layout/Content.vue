<template>
  <div class="content">
    <p><b>Device type: </b>{{ $store.state.ui.device_type }}</p>
    <p>
      {{
        $store.state.user_session.session.account.fullname &&
        $store.state.ui.device_type != 'phone'
      }}
    </p>
  </div>
</template>

<script>
export default {
  name: 'Content',
};
</script>
