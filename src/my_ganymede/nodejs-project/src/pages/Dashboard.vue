<template>
    <p>Dashboard</p>
</template>

<script>
export default {
    name: 'Dashboard',
    mounted() {
        this.$store.commit('update_title', 'Dashboard');
    },
    beforeRouteLeave() {
        this.$store.commit('update_title');
    },
};
</script>