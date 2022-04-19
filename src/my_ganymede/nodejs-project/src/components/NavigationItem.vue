<template>
    <div class="item">
        <div class="icon">
            <i v-bind:class="['fas', icon]"></i>
        </div>
        <div class="text"><slot></slot></div>
    </div>
</template>

<script>
export default {
    name: 'NavigationItem',
    props: {
        icon: {
            type: String,
            mandatory: false,
            default: 'fa-angle-right',
        },
    },
};
</script>
