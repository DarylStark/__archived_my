<template>
    <div v-bind:class="['navigation', { hide: !visible }]">
        <NavigationSection title="First section" hide_title>
            <NavigationItem>Dashboard</NavigationItem>
            <NavigationItem>Tags</NavigationItem>
            <NavigationItem>Notes</NavigationItem>
        </NavigationSection>
        <NavigationSection title="Personal">
            <NavigationItem>Social</NavigationItem>
            <NavigationItem>Music</NavigationItem>
        </NavigationSection>
        <NavigationSection title="Personal Development">
            <NavigationItem>Certifications</NavigationItem>
            <NavigationItem>Courses</NavigationItem>
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
