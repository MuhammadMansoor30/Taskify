<template>
    <div class="home d-flex flex-row">
        <sidebar class="col-12 col-lg-2" />

        <data-table v-if="!isLoading" title="Taskify Roles List" tableTitle="Roles" :fields="fields" :items="items" hasCreatePermission="role_add" 
            v-model:showModal="showModal"/>

        <role-create-modal v-model:showModal="showModal" />
        <div v-if="isLoading" class="d-flex justify-content-center align-items-center mb-3 w-100">
            <b-spinner></b-spinner>
        </div>
    </div>

</template>
<script>
import Sidebar from '@/components/Sidebar.vue';
import DataTable from '@/components/DataTable.vue';
import RoleCreateModal from '@/components/RoleCreateModal.vue';
import { mapActions, mapGetters } from 'vuex';

export default {
    components: {
        Sidebar,
        DataTable,
        RoleCreateModal,
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
            ],
            items: null,
            showModal: false,
            isLoading: false,
        }
    },
    methods: {
        ...mapActions(['getRolesData']),
        async getRoles() {
            this.isLoading = true;
            try {
                const data = await this.getRolesData();
                this.items = data;
                this.isLoading = false;
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