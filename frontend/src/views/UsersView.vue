<template>
    <div class="home d-flex flex-row">
        <sidebar class="col-12 col-lg-2" />

        <data-table v-if="!isLoading" title="Taskify Users List" tableTitle="Users" :fields="fields" :items="items"
            :editData="editData" :deleteData="deleteData" has-create-permission="user_create"
            v-model:showModal="showModal" />

        <users-create-edit-modal v-model:showModal="showModal" :data="userData" v-model:editBtn="editBtn"/>

        <div v-if="isLoading" class="d-flex justify-content-center align-items-center mb-3 w-100">
            <b-spinner></b-spinner>
        </div>
    </div>

</template>
<script>
import Sidebar from '@/components/Sidebar.vue';
import DataTable from '@/components/DataTable.vue';
import UsersCreateEditModal from '@/components/UsersCreateEditModal.vue';
import { mapActions, mapGetters } from 'vuex';
import Swal from 'sweetalert2';

export default {
    components: {
        Sidebar,
        DataTable,
        UsersCreateEditModal,
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
            showModal: false,
            editBtn: false,
            userData: null,
            isLoading: false,
        }
    },
    methods: {
        ...mapActions(['getUsersData', 'deleteUser']),
        async editData(data) {
            this.userData = data;
            this.editBtn = true;
            this.showModal = true;
        },
        async deleteData(data) {
            console.log(data.id);
            try {
                const result = await this.deleteUser(data.id);
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
                        title: "Could not delete User some error occurred.",
                        timer: 1000,
                        showConfirmButton: false,
                    });
                }
            }
            catch (error) {
                console.log(error);
            }
        },
        async getUsers() {
            this.isLoading = true;
            try {
                const data = await this.getUsersData();
                this.items = data;
                this.isLoading = false;
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