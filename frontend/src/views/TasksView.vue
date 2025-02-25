<template>
    <div class="home d-flex flex-row">
        <sidebar class="col-12 col-lg-2" />

        <data-table v-if="!isLoading" title="Taskify Tasks List" tableTitle="Tasks" :fields="fields" :items="items"
            :editData="editData" :deleteData="deleteData" hasCreatePermission="task_add"
            v-model:showModal="showModal" />

        <tasks-create-edit-modal v-model:showModal="showModal" />

        <div v-if="isLoading" class="d-flex justify-content-center align-items-center mb-3 w-100">
            <b-spinner></b-spinner>
        </div>
    </div>

</template>
<script>
import Sidebar from '@/components/Sidebar.vue';
import DataTable from '@/components/DataTable.vue';
import TasksCreateEditModal from '@/components/TasksCreateEditModal.vue';
import { mapActions, mapGetters } from 'vuex';
import dayjs from 'dayjs';
import Swal from 'sweetalert2';

export default {
    components: {
        Sidebar,
        DataTable,
        TasksCreateEditModal
    },
    async mounted() {
        this.getTasks();
    },
    data() {
        return {
            fields: [
                { key: 'index', label: "Id", thStyle: { width: '200px', fontSize: "20px", color: "#242124", } },
                { key: 'title', label: 'Title', thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'team', label: "Team", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'is_completed', label: "Is Completed", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'priority', label: "Priority", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'assigned_to', label: "Assigned To", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'duration', label: "Duration Till", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'button', label: "Action", thStyle: { width: '200px', fontSize: "20px", color: "#242124", } },
            ],
            items: null,
            showModal: false,
            isLoading: false,
        }
    },
    methods: {
        ...mapActions(['getTasksData', 'getTeamById', 'deleteTask']),
        editData(data) {
            console.log(data);
        },
        async deleteData(data) {
            console.log(data.id);
            try {
                const result = await this.deleteTask(data.id);
                if (result) {
                    Swal.fire({
                        icon: "success",
                        title: result.Msg,
                        timer: 1500,
                        showCancelButton: false,
                    }).then(() => {
                        window.location.reload();
                    });
                }
                else {
                    Swal.fire({
                        icon: "error",
                        title: "Could not delete Task some error occurred.",
                        timer: 1500,
                        showCancelButton: false,
                    });
                }
            }
            catch (error) {
                console.log(error);
            }
        },
        setCellVariants(data) {
            const priority = data.priority;
            if (priority === 'Low') {
                data._cellVariants = { priority: 'success' };
            }
            else if (priority === 'Medium') {
                data._cellVariants = { priority: 'warning' };
            }
            else if (priority === 'High') {
                data._cellVariants = { priority: 'danger' };
            }
        },
        async getTasks() {
            this.isLoading = true;
            try {
                const data = await this.getTasksData();
                await Promise.all(data.map(async val => {
                    const newDate = dayjs(val.duration).format('DD-MMM-YYYY');
                    if (val.team) {
                        const teamName = await this.getTeamName(val.team);
                        val.team = teamName['name'];
                    }
                    else {
                        val.team = 'None';
                    }
                    this.setCellVariants(val);
                    val.duration = newDate;
                }));
                this.items = data;
                this.isLoading = false;
            }
            catch (error) {
                console.log(error);
            }
        },
        async getTeamName(id) {
            try {
                const data = await this.getTeamById(id);
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