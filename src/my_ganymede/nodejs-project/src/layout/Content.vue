<template>
  <div class="content">
    <p><b>Device type: </b>{{ $store.state.device_type }}</p>
    <p>
      {{
        $store.state.session.account.fullname &&
        $store.state.device_type != 'phone'
      }}
    </p>
  </div>
</template>

<script>
export default {
  name: 'Content',
};
</script>
