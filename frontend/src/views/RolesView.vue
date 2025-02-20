<template>
    <div class="home d-flex flex-row">
        <sidebar class="col-12 col-lg-2" />

        <data-table title="Taskify Roles List" tableTitle="Roles" :fields="fields" :items="items" :editData="editData"
            :deleteData="deleteData" hasCreatePermission="role_add" />

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
        this.getRoles();
    },
    data() {
        return {
            fields: [
                { key: 'index', label: "Id", thStyle: { width: '200px', fontSize: "20px", color: "#242124", } },
                { key: 'name', label: 'Name', thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'code_name', label: "Code Name", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'button', label: "Action", thStyle: { width: '200px', fontSize: "20px", color: "#242124", } },
            ],
            items: null,
        }
    },
    methods: {
        ...mapActions(['getRolesData']),
        editData(data) {
            console.log(data);
        },
        deleteData(data) {
            console.log(data);
        },
        async getRoles() {
            try {
                const data = await this.getRolesData();
                this.items = data;
            }
            catch (error) {
                console.log(error);
            }
        },
        async getTaskName(id) {
            try {
                const data = await this.getTaskById(id);
                return data;
            }
            catch (error) {
                console.log(error);
            }
        }
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