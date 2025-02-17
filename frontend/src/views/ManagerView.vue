<template>
  <div class="home d-flex">
    <sidebar :navItems="navItems" :navigateTo="navigateTo"></sidebar>

    <div class="flex-grow-1 p-3">
      <h2 class="my-4">Manager Page</h2>
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/Sidebar.vue';

export default {
  // We can pass items that are used in entire application from the App component to all teh components using router-view props. To access then in any component just call the props name and we can access the properties or data defined in the App file.
  props: ['navItems', 'navigateTo'],
  components: {
    Sidebar,
  },
};
</script>

<style scoped>
.home {
  display: flex;
  min-height: 100vh;
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

.flex-grow-1 {
  margin-left: 250px;
  /* Leave space for the sidebar */
}

.b-button {
  margin-bottom: 20px;
}
</style>
