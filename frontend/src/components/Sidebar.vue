<template>
    <div>
        <div class="sidebar text-dark">
            <b-navbar toggleable="lg" type="light" class="border-bottom">
                <b-navbar-brand href="#" class="font-weight-bold">
                    Taskify Functions
                </b-navbar-brand>
            </b-navbar>

            <b-nav vertical>
                <b-nav-item v-for="(item, index) in navItems" :key="index" href="#"
                    @click.prevent="navigateTo(item.route);" :class="{ active: item.title === this.$route.meta.title }"
                    class="sidebar-nav-item py-2 px-3 d-flex flex-row ">
                    <i :class="item.icon"></i>
                    <span
                        :class="{ 'text-dark': item.title !== this.$route.meta.title, 'text-light': item.title === this.$route.meta.title }"
                        class="m-3 font-weight-bold h4">{{ item.title }}</span>
                </b-nav-item>
            </b-nav>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    methods: {
        ...mapGetters(['getNavMenuItems']),
        navigateTo(page) {
            this.$router.push({ name: page });
        },
    },
    data() {
        return {
            navItems: this.getNavMenuItems(),
        }
    },
};
</script>

<style scoped>
.sidebar {
    width: 320px;
    padding-top: 30px;
    position: fixed;
    height: 100%;
    left: 0;
    top: 0;
    background-color: #e2dbd4;
    box-shadow: 2px 0px 5px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}

.sidebar .b-navbar {
    padding: 1rem;
    background-color: #343a40;
    color: #e2dbd4;
}

.sidebar .b-navbar-brand {
    font-size: 1.5rem;
}

.sidebar .b-nav-item {
    cursor: pointer;
    padding: 10px 20px;
    font-size: 1.1rem;
    border-bottom: 1px solid #ddd;
    transition: background-color 0.3s ease, color 0.3s ease;
}

.sidebar .b-nav-item:hover {
    background-color: #007bff;
    color: #e2dbd4;
}

.sidebar .b-nav-item.active {
    background-color: #0056b3;
    color: #e2dbd4;
}

.flex-grow-1 {
    margin-left: 280px;
}

.sidebar-nav-item i {
    font-size: 1.5rem;
    color: #800020;
}

.sidebar-nav-item:hover {
    background-color: #f1f1f1;
}

.sidebar-nav-item.active {
    background-color: #800020;
    color: #e2dbd4;
}

.sidebar-nav-item.active i {
    color: #e2dbd4;
}

.sidebar .b-nav-item+.b-nav-item {
    margin-top: 5px;
}
</style>


<!-- #242124  Color for text-->