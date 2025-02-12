<template>
    <div class="home d-flex">
        <div class="sidebar bg-light text-dark">
            <b-navbar toggleable="lg" type="light" variant="light" class="border-bottom">
                <b-navbar-brand href="#" class="font-weight-bold">
                    Taskify
                </b-navbar-brand>
            </b-navbar>

            <b-nav vertical>
                <b-nav-item v-for="(item, index) in navItems" :key="index" href="#"
                    @click.prevent="navigateTo(item.route)" class="sidebar-nav-item">
                    <i :class="item.icon" class="mr-5"></i>{{ item.title }}
                </b-nav-item>
            </b-nav>
        </div>
    </div>
</template>

<script>
export default {
    props: ['navItems', 'navigateTo'],
};
</script>

<style scoped>
.sidebar {
    width: 280px;
    padding-top: 30px;
    position: fixed;
    height: 100%;
    left: 0;
    top: 0;
    background-color: #f8f9fa;
    box-shadow: 2px 0px 5px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}

.sidebar .b-navbar {
    padding: 1rem;
    background-color: #343a40;
    color: white;
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
    color: white;
}

.sidebar .b-nav-item.active {
    background-color: #0056b3;
    color: white;
}

.flex-grow-1 {
    margin-left: 280px;
}

.sidebar-nav-item i {
    font-size: 1.2rem;
    color: #6c757d;
}

.sidebar-nav-item:hover i {
    color: white;
}

.sidebar .b-nav-item+.b-nav-item {
    margin-top: 5px;
}
</style>