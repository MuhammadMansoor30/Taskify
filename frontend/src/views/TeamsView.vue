<template>
    <div class="home d-flex flex-row">
        <sidebar class="col-12 col-lg-2" />

        <data-table v-if="!isLoading" title="Taskify Teams List" tableTitle="Teams" :fields="fields" :items="items"
            :editData="editData" :deleteData="deleteData" hasCreatePermission="team_add"
            v-model:showModal="showModal" hasEditPermission="team_edit"/>

        <team-create-edit-modal v-model:showModal="showModal" :data="teamData" v-model:editBtn="editBtn" />

        <div v-if="isLoading" class="d-flex justify-content-center align-items-center mb-3 w-100">
            <b-spinner></b-spinner>
        </div>

    </div>

</template>
<script>
import Sidebar from '@/components/Sidebar.vue';
import DataTable from '@/components/DataTable.vue';
import TeamCreateEditModal from '@/components/TeamCreateEditModal.vue';
import { mapActions, mapGetters } from 'vuex';
import Swal from 'sweetalert2';

export default {
    components: {
        Sidebar,
        DataTable,
        TeamCreateEditModal,
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
            showModal: false,
            editBtn: false,
            teamData: null,
            isLoading: false,
        }
    },
    methods: {
        ...mapActions(['getTeamsData', 'getManagerById', 'deleteTeam', 'getTeamById']),
        async editData(data) {
            const team = await this.getTeamById(data.id);    // Fecthing team data again to get manager id as it has been replaced with name here.
            this.teamData = team;
            this.editBtn = true;
            this.showModal = true;
        },
        async deleteData(data) {
            console.log("Deleting: ", data, " id ", data.id);
            try {
                const result = await this.deleteTeam(data.id);
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
                        title: "Could not delete Team some error occurred.",
                        timer: 1500,
                        showCancelButton: false,
                    });
                }
            }
            catch (error) {
                console.log(error);
            }
        },
        async getTeams() {
            this.isLoading = true;
            try {
                const data = await this.getTeamsData(); 
                // Due to the reactivity system of Vue to cause changes and modify the items we have to wait for the promise to resolve and then our items will be updated else old data withour chnages will be passed.
                await Promise.all(data.map(async val => {
                    const manager = await this.getManagerId(val.manager);
                    val.manager = manager['full_name'];
                }));
                this.items = data;
                this.isLoading = false;
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