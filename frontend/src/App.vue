<template>
  <router-view />
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
  },

  // Can also add all the getData actions from store to fecth all the data at the start of app and then use getters to fetch data where needed inside of app.
  // Or follow the approach followed here of fecthing data in individual components and views. Both are correct and based on choice can be selected.
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
