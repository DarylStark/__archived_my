<template>
    <p><b>404 ERROR</b>: Unknown page</p>
</template>

<script>
export default {
    name: 'Dashboard',
    mounted() {
        this.$store.commit('update_title', 'Error 404');
    },
    beforeRouteLeave() {
        this.$store.commit('update_title');
    },
};
</script>