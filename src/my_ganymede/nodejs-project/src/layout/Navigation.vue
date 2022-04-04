<template>
    <div v-bind:class="['navigation', { hide: !visible }]">
        <NavigationSection title="First section" hide_title>
            <NavigationItem>Item 1</NavigationItem>
            <NavigationItem>Item 2</NavigationItem>
        </NavigationSection>
        <NavigationSection title="Second section">
            <NavigationItem>Item 3</NavigationItem>
            <NavigationItem>Item 4</NavigationItem>
            <NavigationItem>Item 5</NavigationItem>
        </NavigationSection>
    </div>
</template>

<script>
import NavigationItem from '../components/NavigationItem.vue';
import NavigationSection from '../components/NavigationSection.vue';

export default {
    name: 'Navigation',
    computed: {
        visible() {
            return this.$store.state.ui.navigation_visible;
        },
    },
    components: {
        NavigationItem,
        NavigationSection,
    },
};
</script>
