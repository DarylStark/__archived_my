<template>
    <div class="item">
        <div class="icon">
            <i class="fas fa-user-circle"></i>
        </div>
        <div class="text"><slot></slot></div>
    </div>
</template>

<script>
export default {
    name: 'NavigationItem',
};
</script>
