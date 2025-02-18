<template>
  <div class="home d-flex flex-row">
    <sidebar class="col-12 col-lg-2" />

    <div class="d-flex flex-column w-100">
      <div class="p-3">
        <h2 class="my-4">Taskify Managers List</h2>
      </div>
      <div class="container-fluid my-5">
        <div class="card shadow-sm">
          <div class="card-header" style="background-color: #800020; color: #ececec;">
            <h4 class="mb-0">Managers</h4>
          </div>
          <div class="card-body">
            <b-table :fields="fields" :items="items" responsive="sm" class="table table-bordered table-hover table-lg">
              <template #cell(button)="data">
                <button class="btn btn-primary">Action</button>
              </template>

              <template #cell(index)="data">
                <span class=" text-primary font-weight-bold fs-4">{{ data.index + 1 }}</span>
              </template>

              <template #cell()="data">
                <span class="text-muted font-weight-bold fs-4">{{ data.value }}</span>
              </template>
            </b-table>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import Sidebar from '@/components/Sidebar.vue';
import { mapGetters } from 'vuex';

export default {
  mounted() {
    console.log(this.hasPermissions('user_create'))
  },
  // We can pass items that are used in entire application from the App component to all teh components using router-view props. To access then in any component just call the props name and we can access the properties or data defined in the App file. Not used here at the moment
  // props: ['navItems', 'navigateTo'],
  data() {
    return {
      fields: [
        {key: 'button', label: "Action", thStyle: { width: '200px', fontSize: "20px" }},
        {key: 'index', label: "Index", thStyle: { width: '200px', fontSize: "20px" } }, 
        { key: 'name', label: 'Full Name', thStyle: { fontSize: "20px" } },
        {key: 'experience', label: "Experience", thStyle: { fontSize: "20px" } },
        {key: 'department', label: "Department", thStyle: { fontSize: "20px" } },
      ],
      items: [
        { name: 'John', experience: 'Male', department: "Abc" },
        { name: 'Jane', experience: 'Female', department: "Abc" },
        { name: 'Rubin', experience: 'Male', department: "Abc" },
        { name: 'Shirley', experience: 'Female', department: "Abc" }
      ]
    }
  },
  components: {
    Sidebar,
  },
  computed: {
    ...mapGetters(['hasPermissions']),
  }
};
</script>

<style scoped>
.home {
  min-height: 100vh;
  max-height: 100vh;
}

.sidebar {
  width: 400px;
  padding-top: 20px;
  position: fixed;
  height: 100%;
  left: 0;
  top: 0;
  background-color: #f8f9fa;
  box-shadow: 2px 0px 5px rgba(0, 0, 0, 0.1);
}

.sidebar .b-nav-item {
  cursor: pointer;
}

/* .ttle-1 {
  margin-left: 250px;
}

.ttle-2 {
  margin-left: 400px;
} */

.b-button {
  margin-bottom: 20px;
}
</style>
