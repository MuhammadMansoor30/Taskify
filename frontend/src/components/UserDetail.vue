<template>
    <div class="text-center">
        <h5 class="fw-bold fs-3">{{ name }}</h5>
    </div>
    <div>
    </div>
    <strong class="fs-5">Role:</strong>{{ role }}
    <strong class="ms-2">Email:</strong><a :href="'mailto:' + email" class="fs-5">{{ email }}</a>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    mounted() {
        const user = this.getUser;
        this.name = user.username;
        this.role = user.roles[0].name;
        this.email = user.email;
    },
    name: 'UserCard',
    data() {
        return {
            name: '',
            role: '',
            email: '',
        };
    },
    computed: {
        ...mapGetters(['getUser']),
    },
};
</script>

<style scoped>
a {
    text-decoration: none;
    color: #007bff;
}

a:hover {
    text-decoration: underline;
}
</style>