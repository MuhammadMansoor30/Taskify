<template>
    <div class="home d-flex flex-row">
        <sidebar class="col-12 col-lg-2" />

        <data-table v-if="!isLoading" title="Taskify Approve Work Items List" tableTitle="Work Items For Approval" :fields="fields"
            :items="items" :approve-work="approveWork" hasApprovalPermission="approve_work" />

        <!-- We can pass in props that are rrequired and dont have to define all and only those will have values which are defined else will be null same as in React -->

        <div v-if="isLoading" class="d-flex justify-content-center align-items-center mb-3 w-100">
            <b-spinner></b-spinner>
        </div>
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
        this.getWorkItems();
    },
    data() {
        return {
            fields: [
                { key: 'index', label: "Id", thStyle: { width: '200px', fontSize: "20px", color: "#242124", } },
                { key: 'name', label: 'Name', thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'fileName', label: "Work Item", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'status', label: "Status", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'is_approved', label: "Is Approved", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'task', label: "Task", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'button', label: "Action", thStyle: { width: '200px', fontSize: "20px", color: "#242124", } },
            ],
            items: null,
            isLoading: false,
        }
    },
    methods: {
        ...mapActions(['getWorkItemsData', 'getTaskById']),
        approveWork(data) {
            console.log(data);
        },
        async getWorkItems() {
            this.isLoading = true;
            try {
                const data = await this.getWorkItemsData({ is_approved: false });   // Fetch only not approved Work Items
                await Promise.all(data.map(async val => {
                    const fileName = val.file.split('/')[2];
                    const taskName = await this.getTaskName(val.task);
                    val.fileName = fileName;   // Adding new fileName file data final data for display.
                    val.task = taskName['title'];
                }));
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