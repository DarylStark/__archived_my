<template>
    <div class="item" v-on:click="go_to_page">
        <div class="icon">
            <i v-bind:class="['fas', icon]"></i>
        </div>
        <div class="text"><slot></slot></div>
    </div>
</template>

<script>
export default {
    name: 'NavigationItem',
    methods: {
        go_to_page() {
            // Navigate to the specified page
            this.$router.push(this.href);
        },
    },
    props: {
        icon: {
            type: String,
            mandatory: false,
            default: 'fa-angle-right',
        },
        href: {
            type: String,
            mandatory: true,
        },
    },
};
</script>
