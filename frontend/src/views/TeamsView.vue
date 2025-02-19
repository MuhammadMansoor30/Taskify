<template>
    <div class="home d-flex flex-row">
        <sidebar class="col-12 col-lg-2" />

        <data-table title="Taskify Teams List" tableTitle="Teams" :fields="fields" :items="items" :editData="editData"
            :deleteData="deleteData" hasCreatePermission="team_add" />

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
    mounted() {
        this.getTeams();
    },
    data() {
        return {
            fields: [
                { key: 'index', label: "Id", thStyle: { width: '200px', fontSize: "20px", color: "#242124", } },
                { key: 'name', label: 'Name', thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'project_name', label: "Project Name", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'manager', label: "Manager", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'button', label: "Action", thStyle: { width: '200px', fontSize: "20px", color: "#242124", } },
            ],
            items: null,
        }
    },
    methods: {
        ...mapActions(['getTeamsData', 'getManagerById']),
        editData(data) {
            console.log(data);
        },
        deleteData(data) {
            console.log(data);
        },
        async getTeams() {
            try {
                const data = await this.getTeamsData();
                // Due to the reactivity system of Vue to cause changes and modify the items we have to wait for the promise to resolve and then our items will be updated else old data withour chnages will be passed.
                await Promise.all(data.map(async val =>{
                    const manager = await this.getManagerId(val.manager);
                    val.manager = manager['full_name'];
                }));  
                this.items = data;
            }
            catch (error) {
                console.log(error);
            }
        },
        async getManagerId(id) {
            try {
                const data = await this.getManagerById({ id });
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