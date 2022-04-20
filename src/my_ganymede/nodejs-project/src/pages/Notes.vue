<template>
    <p>Notes</p>
</template>

<script>
export default {
    name: 'Notes',
    mounted() {
        this.$store.commit('update_title', 'Notes');
    },
    beforeRouteLeave() {
        this.$store.commit('update_title');
    },
};
</script>