<template>
  <router-view :navItems="navItems" :navigateTo="navigateTo" />
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  mounted(){
    this.loadUserData();
    // this.currentUser();
    this.$store.commit('setNavMenuItems');
  },
  methods: {
    ...mapActions(['loadUserData', 'currentUser']),
    ...mapGetters(['hasPermissions', 'getNavMenuItems']),
    navigateTo(page) {
      console.log(page);
      this.$router.push({ name: page });
    },
  },
  data() {
    return {
      navItems: this.getNavMenuItems(),
    }
  },
}

</script>


<style>
#app {
  font-family: 'Afacad', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #e2dbd4;
  text-align: center;
  color: #800020;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #800020;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
