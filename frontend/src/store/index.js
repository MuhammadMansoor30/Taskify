import { createStore } from 'vuex'
import { loginApi } from '@/backendApi';
import Cookies from 'js-cookie';

export default createStore({
  state: {
    isLoggedIn: false,
    user: null,
    navMenuItems: [],
  },

  getters: {
    getUser:  state => {
      return state.user;
    },
    getIsLoggedIn: state => {
      return state.isLoggedIn;
    },
    hasPermissions: state => {
      return state.user.permissions;
    },
    getNavMenuItems: state => {
      return state.navMenuItems;
    }
  },

  mutations: {
    login: (state, data) => {
      state.isLoggedIn = true;
      state.user = data;
    },

    setCookies: (state, data) => {
      Cookies.set('user', JSON.stringify(data.User), {expires: 7, path: ''});
      Cookies.set('isLoggedIn', true, {expires: 7, path: ''});
    },

    setNavMenuItems: (state) => {
      state.navMenuItems = [];

      if (state.user.permissions.includes('manager_get')){
        state.navMenuItems.push({ title: "Mananger", route: "manager", icon: "fas fa-home" });
      }
      if (state.user.permissions.includes('teams_get')){
        state.navMenuItems.push({ title: "Teams", route: "team", icon: "fas fa-home" });
      }
      if (state.user.permissions.includes('work_get')){
        state.navMenuItems.push({ title: "Work", route: "work", icon: "fas fa-home" });
      }
      if (state.user.permissions.includes('developers_get')){
        state.navMenuItems.push({ title: "Developers", route: "developer", icon: "fas fa-home" });
      }
      if (state.user.permissions.includes('tasks_get')){
        state.navMenuItems.push({ title: "Tasks", route: "task", icon: "fas fa-home" });
      }
      if (state.user.permissions.includes('teams_get')){
        state.navMenuItems.push({ title: "Teams", route: "team", icon: "fas fa-home" });
      }
      if (state.user.permissions.includes('user_create')){
        state.navMenuItems.push({ title: "Users", route: "user", icon: "fas fa-home" });
      }
      if (state.user.permissions.includes('teams_get')){
        state.navMenuItems.push({ title: "Teams", route: "team", icon: "fas fa-home" });
      }
      if (state.user.permissions.includes('work_publish')){
        state.navMenuItems.push({ title: "Publish Work", route: "publishWork", icon: "fas fa-home" });
      }
      if (state.user.permissions.includes('approve_work')){
        state.navMenuItems.push({ title: "Approve Work", route: "approveWork", icon: "fas fa-home" });
      }
      if (state.user.permissions.includes('roles_get')){
        state.navMenuItems.push({ title: "Roles", route: "role", icon: "fas fa-home" });
      }
    }
  },

  actions: {
    login: async (context, data) => {
      try{
        const res = await loginApi.post('login/', data);
        if (res.status === 200 && res.data.User){
          context.commit('login', res.data.User);
          context.commit('setNavMenuItems');
          // context.commit('setCookies', res.data);
          return res.data;
        }
      }
      catch (error){
        console.log(error);
      }
    },

    currentUser: async (context) => {
      try{
        const res = await  loginApi.get('currentuser/');
        if(res.status === 200 && res.data.User){
          context.commit('login', res.data.User);
          context.commit('setNavMenuItems');
          return res.data;
        }
      }
      catch (error){
        console.log(error);
      }
    },

    loadCookies: (context, data) => {
      const user = Cookies.get('user');
      const isLoggedIn = Cookies.get('isLoggedIn');
      
      if(user && isLoggedIn){
        context.commit('login', JSON.parse(user));
      }
    }
  },
})
