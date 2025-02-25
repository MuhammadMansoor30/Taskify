<template>
    <div class="home d-flex flex-row">
        <sidebar class="col-12 col-lg-2" />

        <data-table v-if="!isLoading" title="Taskify Developers List" tableTitle="Developers" :fields="fields" :items="items"
            :editData="editData" :deleteData="deleteData" hasCreatePermission="developer_add" v-model:showModal="showModal" />

        <developers-create-edit-modal v-model:showModal="showModal"/>

        <div v-if="isLoading" class="d-flex justify-content-center align-items-center mb-3 w-100">
            <b-spinner></b-spinner>
        </div>
    </div>

</template>
<script>
import Sidebar from '@/components/Sidebar.vue';
import DataTable from '@/components/DataTable.vue';
import DevelopersCreateEditModal from '@/components/DevelopersCreateEditModal.vue';
import { mapActions, mapGetters } from 'vuex';
import Swal from 'sweetalert2';

export default {
    components: {
        Sidebar,
        DataTable,
        DevelopersCreateEditModal,
    },
    async mounted() {
        this.getDevelopers();
    },
    data() {
        return {
            fields: [
                { key: 'index', label: "Id", thStyle: { width: '200px', fontSize: "20px", color: "#242124", } },
                { key: 'full_name', label: 'Name', thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'experience', label: "Experience", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'skill_set', label: "Skill Set", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'manager', label: "Manager", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'team', label: "Team", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'button', label: "Action", thStyle: { width: '200px', fontSize: "20px", color: "#242124", } },
            ],
            items: null,
            showModal: false,
            isLoading: false,
        }
    },
    methods: {
        ...mapActions(['getDevelopersData', 'getManagerById', 'getTeamById', 'deleteDeveloper']),
        editData(data) {
            console.log(data);
            // this.showModal = true;
        },
        async deleteData(data) {
            try{
                const result = await this.deleteDeveloper(data.id);
                if(result){
                    Swal.fire({
                        icon: 'success',
                        timer: 1500,
                        title: result.Msg,
                        showCancelButton: false,
                    }).then(() => {
                        this.$emit('update:showModal', false);
                        location.reload();
                    });
                }
                else{
                    Swal.fire({
                        icon: 'error',
                        title: "Could not delete developer some error occurred",
                        timer: 1500,
                        showCancelButton: false,
                    });
                }
            }
            catch(error){
                console.log(error);
            }
        },
        async getDevelopers() {
            this.isLoading = true;
            try {
                const data = await this.getDevelopersData();
                await Promise.all(data.map(async val => {
                    if (val.manager && val.team) {
                        const managerName = await this.getManagerId(val.manager);
                        const teamName = await this.getTeamName(val.team);
                        val.manager = managerName['full_name'];
                        val.team = teamName['name'];
                    }
                    else {
                        val.manager = 'None';
                        val.team = 'None';
                    }
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