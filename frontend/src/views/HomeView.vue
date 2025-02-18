<template>
  <div class="home d-flex">
    <sidebar></sidebar>

    <div class="flex-grow-1 p-3">
      <h2 class="my-4">Welcome To Taskify</h2>
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/Sidebar.vue';

export default {
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
