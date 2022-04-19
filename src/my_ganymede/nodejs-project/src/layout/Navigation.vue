<template>
    <div v-bind:class="['navigation', { hide: !visible }]">
        <NavigationSection title="My" hide_title>
            <NavigationItem icon="fa-list">Dashboard</NavigationItem>
            <NavigationItem icon="fa-tags">Tags</NavigationItem>
            <NavigationItem icon="fa-book-open">Notes</NavigationItem>
        </NavigationSection>
        <NavigationSection title="Personal">
            <NavigationItem icon="fa-user-group">Social</NavigationItem>
            <NavigationItem icon="fa-music">Music</NavigationItem>
            <NavigationItem icon="fa-chart-line">Finances</NavigationItem>
            <i class="fa-solid"></i>
        </NavigationSection>
        <NavigationSection title="Personal Development">
            <NavigationItem icon="fa-graduation-cap"
                >Certifications</NavigationItem
            >
            <NavigationItem icon="fa-school">Courses</NavigationItem>
        </NavigationSection>
        <NavigationSection title="Professional">
            <NavigationItem icon="fa-building">Jobs</NavigationItem>
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
