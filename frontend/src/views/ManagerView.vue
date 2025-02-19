<template>
  <div class="home d-flex flex-row">
    <sidebar class="col-12 col-lg-2" />

    <data-table title="Taskify Managers List" tableTitle="Managers" :fields="fields" :items="items" :editData="editData"
      :deleteData="deleteData" hasCreatePermission="user_create" />

  </div>

</template>

<script>
import Sidebar from '@/components/Sidebar.vue';
import DataTable from '@/components/DataTable.vue';
import { mapActions, mapGetters } from 'vuex';

export default {
  // We can pass items that are used in entire application from the App component to all teh components using router-view props. To access then in any component just call the props name and we can access the properties or data defined in the App file. Not used here at the moment
  // props: ['navItems', 'navigateTo'],
  async mounted() {
    await this.getManagers;
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
    }
  },
  components: {
    Sidebar,
    DataTable,
  },
  computed: {
    ...mapGetters(['hasPermissions']),
    ...mapActions(['getManagersData']),
    async getManagers() {
      try {
        const data = await this.getManagersData;
        this.items = data;
      }
      catch (error) {
        console.log(error);
      }
    }
  },
  methods: {
    editData(data) {
      console.log(data);
    },
    deleteData(data) {
      console.log(data);
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
