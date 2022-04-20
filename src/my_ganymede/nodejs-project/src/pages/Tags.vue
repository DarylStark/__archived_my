<template>
    <p>Tags</p>
</template>

<script>
export default {
    name: 'Tags',
    mounted() {
        this.$store.commit('update_title', 'Tags');
    },
    beforeRouteLeave() {
        this.$store.commit('update_title');
    },
};
</script>