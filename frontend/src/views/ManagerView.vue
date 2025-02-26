<template>
  <div class="home d-flex flex-row">
    <sidebar class="col-12 col-lg-2" />

    <data-table v-if="!isLoading" title="Taskify Managers List" tableTitle="Managers" :fields="fields" :items="items"
      :editData="editData" :deleteData="deleteData" hasCreatePermission="user_create" v-model:showModal="showModal" />

    <manager-create-edit-modal v-model:showModal="showModal" :data="managerData" v-model:editBtn="editBtn"  />

    <div v-if="isLoading" class="d-flex justify-content-center align-items-center mb-3 w-100">
      <b-spinner></b-spinner>
    </div>
  </div>

</template>

<script>
import Sidebar from '@/components/Sidebar.vue';
import DataTable from '@/components/DataTable.vue';
import ManagerCreateEditModal from '@/components/ManagerCreateEditModal.vue';
import { mapActions, mapGetters } from 'vuex';
import Swal from 'sweetalert2';

export default {
  // We can pass items that are used in entire application from the App component to all the components using router-view props. To access them in any component just call the props name and we can access the properties or data defined in the App file. Not used here at the moment
  // props: ['navItems', 'navigateTo'],
  async mounted() {
    await this.getManagers;
  },
  components: {
    Sidebar,
    DataTable,
    ManagerCreateEditModal
  },
  data() {
    return {
      fields: [
        { key: 'index', label: "Id", thStyle: { width: '200px', fontSize: "20px", color: "#242124", } },
        { key: 'full_name', label: 'Full Name', thStyle: { fontSize: "20px", color: "#242124", } },
        { key: 'experience', label: "Experience", thStyle: { fontSize: "20px", color: "#242124", } },
        { key: 'department', label: "Department", thStyle: { fontSize: "20px", color: "#242124", } },
        { key: 'button', label: "Action", thStyle: { width: '200px', fontSize: "20px", color: "#242124", } },
      ],
      items: null,
      showModal: false,
      editBtn: false,
      managerData: null,
      isLoading: false,
    }
  },
  computed: {
    ...mapGetters(['hasPermissions']),
    async getManagers() {
      this.isLoading = true;
      try {
        const data = await this.getManagersData();
        this.items = data;
        this.isLoading = false;
      }
      catch (error) {
        console.log(error);
      }
    }
  },
  methods: {
    ...mapActions(['getManagersData', 'deleteManager', 'getUserById']),
    async editData(data) {
      const user = await this.getUserById(data.user);
      this.managerData = {data, user};
      this.editBtn = true;
      this.showModal = true;
    },
    async deleteData(data) {
      try {
        const result = await this.deleteManager(data.id);
        if (result) {
          Swal.fire({
            icon: "success",
            title: result.Msg,
            timer: 2000,
            showCancelButton: false,
          }).then(() => {
            window.location.reload();
          });
        }
        else {
          Swal.fire({
            icon: 'error',
            title: "Could Not Delete Manager Some Error Occurred",
            timer: 2000,
            showCancelButton: false,
          });
        }
      }
      catch (error) {
        console.log(error);
      }
    },
  }
};
</script>

<style scoped>
.home {
  min-height: 100vh;
  max-height: 100%;
}
</style>
