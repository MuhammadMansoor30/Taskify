<template>
    <div class="home d-flex flex-row">
        <sidebar class="col-12 col-lg-2" />

        <data-table title="Taskify Users List" tableTitle="Users" :fields="fields" :items="items" :editData="editData"
            :deleteData="deleteData" has-create-permission="user_create" />

    </div>

</template>
<script>
import Sidebar from '@/components/Sidebar.vue';
import DataTable from '@/components/DataTable.vue';
import { mapActions, mapGetters } from 'vuex';

export default {
    components: {
        Sidebar,
        DataTable
    },
    async mounted() {
        this.getUsers();
    },
    data() {
        return {
            fields: [
                { key: 'index', label: "Id", thStyle: { width: '200px', fontSize: "20px", color: "#242124", } },
                { key: 'username', label: 'Name', thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'email', label: "Email Address", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'cnic', label: "CNIC", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'mobile_no', label: "Contact Number", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'button', label: "Action", thStyle: { width: '200px', fontSize: "20px", color: "#242124", } },
            ],
            items: null,
        }
    },
    methods: {
        ...mapActions(['getUsersData']),
        editData(data) {
            console.log(data);
        },
        deleteData(data) {
            console.log(data);
        },
        async getUsers() {
            try {
                const data = await this.getUsersData();
                this.items = data;
            }
            catch (error) {
                console.log(error);
            }
        },
    },
    computed: {
        ...mapGetters(['hasPermissions']),
    },
};
</script>

<style scoped>
.home {
    display: flex;
    min-height: 100vh;
}
</style>