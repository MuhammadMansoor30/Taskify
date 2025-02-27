<template>
    <div>
        <div class="sidebar text-dark">
            <div class="py-3 me-3">
                <user-detail />
            </div>

            <b-navbar toggleable="lg" type="light" class="border-bottom">
                <b-navbar-brand href="#" class="font-weight-bold">
                    Taskify Functions
                </b-navbar-brand>
            </b-navbar>

            <b-nav vertical>
                <b-nav-item v-for="(item, index) in navItems" :key="index" href="#"
                    @click.prevent="navigateTo(item.route);" :class="{ active: item.title === this.$route.meta.title }"
                    class="sidebar-nav-item d-flex flex-row p-2 mx-1 rounded-4">
                    <i :class="item.icon"></i>
                    <span
                        :class="{ 'text-dark': item.title !== this.$route.meta.title, 'text-light': item.title === this.$route.meta.title }"
                        class="m-3 font-weight-bold h4">{{ item.title }}</span>
                </b-nav-item>
            </b-nav>
            <button class="btn btn-success my-5 mx-3 fs-5 rounded-5" @click="signOut()">Sign Out</button>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
import UserDetail from './UserDetail.vue';

export default {
    components: {
        UserDetail
    },
    methods: {
        ...mapGetters(['getNavMenuItems']),
        navigateTo(page) {
            this.$router.push({ name: page });
        },
        async signOut() {
            try {
                const res = await this.$store.dispatch("logout");
                this.$router.replace({ name: 'login' });   // To remove all the previous router history
                return res;
            }
            catch (error) {
                console.log(error);
            }
        }
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
    display: flex;
    flex-direction: column;
    width: 320px;
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