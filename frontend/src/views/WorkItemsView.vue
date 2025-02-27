<template>
    <div class="home d-flex flex-row">
        <sidebar class="col-12 col-lg-2" />

        <data-table v-if="!isLoading" title="Taskify Work Items List" tableTitle="Work Items" :fields="fields"
            :items="items" :editData="editData" :deleteData="deleteData" />

        <work-item-edit-modal v-model:showModal="showModal" :data="workItemData"/>

        <div v-if="isLoading" class="d-flex justify-content-center align-items-center mb-3 w-100">
            <b-spinner></b-spinner>
        </div>
    </div>

</template>
<script>
import Sidebar from '@/components/Sidebar.vue';
import DataTable from '@/components/DataTable.vue';
import WorkItemEditModal from '@/components/WorkItemEditModal.vue';
import { mapActions, mapGetters } from 'vuex';
import Swal from 'sweetalert2';

export default {
    components: {
        Sidebar,
        DataTable,
        WorkItemEditModal,
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
                { key: 'is_approved', label: "Is Approved", thStyle: { width: '120px', fontSize: "20px", color: "#242124", } },
                { key: 'task', label: "Task", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'button', label: "Action", thStyle: { width: '200px', fontSize: "20px", color: "#242124", } },
            ],
            items: null,
            showModal: false,
            workItemData: null,
            isLoading: false,
        }
    },
    methods: {
        ...mapActions(['getWorkItemsData', 'getTaskById', 'deleteWorkIten', 'getWorkItemById']),
        async editData(data) {
            const dta = await this.getWorkItemById(data.id);
            this.workItemData = dta;
            this.showModal = true;
        },
        async deleteData(data) {
            try {
                const result = await this.deleteWorkIten(data.id);
                if (result) {
                    Swal.fire({
                        icon: "success",
                        title: result.Msg,
                        timer: 1000,
                        showConfirmButton: false,
                    }).then(() => {
                        window.location.reload();
                    });
                }
                else {
                    Swal.fire({
                        icon: "error",
                        title: "Could not delete Work Item some error occurred.",
                        timer: 1000,
                        showConfirmButton: false,
                    });
                }
            }
            catch (error) {
                console.log(error);
            }
            console.log(data);
        },
        async getWorkItems() {
            this.isLoading = true;
            try {
                const data = await this.getWorkItemsData();   // Fetch only approved Work Items
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