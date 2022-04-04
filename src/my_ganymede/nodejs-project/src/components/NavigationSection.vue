<template>
    <div>
        <div class="title" v-if="!hide_title">{{ title }}</div>
        <slot></slot>
    </div>
</template>

<script>
export default {
    name: 'NavigationSection',
    props: {
        title: String,
        hide_title: {
            type: Boolean,
            default: false,
        },
    },
};
</script>
