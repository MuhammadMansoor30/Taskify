<template>
    <div class="home d-flex flex-row">
        <sidebar class="col-12 col-lg-2" />

        <data-table title="Taskify Tasks List" tableTitle="Tasks" :fields="fields" :items="items" :editData="editData"
            :deleteData="deleteData" hasCreatePermission="task_add" />

    </div>

</template>
<script>
import Sidebar from '@/components/Sidebar.vue';
import DataTable from '@/components/DataTable.vue';
import { mapActions, mapGetters } from 'vuex';
import dayjs from 'dayjs';

export default {
    components: {
        Sidebar,
        DataTable
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
        }
    },
    methods: {
        ...mapActions(['getTasksData', 'getTeamById']),
        editData(data) {
            console.log(data);
        },
        deleteData(data) {
            console.log(data);
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
            try {
                const data = await this.getTasksData();
                await Promise.all(data.map(async val => {
                    const newDate = dayjs(val.duration).format('DD-MMM-YYYY');
                    if (val.team){
                        const teamName = await this.getTeamName(val.team);
                        val.team = teamName['name'];
                    }
                    else{
                        val.team = 'None';
                    }
                    this.setCellVariants(val);
                    val.duration = newDate;
                }));
                this.items = data;
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