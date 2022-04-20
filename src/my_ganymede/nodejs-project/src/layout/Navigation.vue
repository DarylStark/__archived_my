<template>
    <div v-bind:class="['navigation', { hide: !visible }]">
        <NavigationSection title="My" hide_title>
            <NavigationItem icon="fa-list" href="/dashboard"
                >Dashboard</NavigationItem
            >
            <NavigationItem icon="fa-tags" href="/tags">Tags</NavigationItem>
            <NavigationItem icon="fa-book-open" href="/notes"
                >Notes</NavigationItem
            >
        </NavigationSection>
        <NavigationSection title="Personal">
            <NavigationItem icon="fa-user-group" href="/social"
                >Social</NavigationItem
            >
            <NavigationItem icon="fa-music" href="/music">Music</NavigationItem>
            <NavigationItem icon="fa-chart-line" href="/finances"
                >Finances</NavigationItem
            >
            <i class="fa-solid"></i>
        </NavigationSection>
        <NavigationSection title="Personal Development">
            <NavigationItem icon="fa-graduation-cap" href="/certifications"
                >Certifications</NavigationItem
            >
            <NavigationItem icon="fa-school" href="/courses"
                >Courses</NavigationItem
            >
        </NavigationSection>
        <NavigationSection title="Professional">
            <NavigationItem icon="fa-building" href="/jobs"
                >Jobs</NavigationItem
            >
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
