import { createStore } from 'vuex'
import { backendApi, fileApi, loginApi } from '@/backendApi';
// import Cookies from 'js-cookie';    // Have to install js-cookie to use cookies

export default createStore({
  state: {
    isLoggedIn: false,
    user: null,
    navMenuItems: [],
    managers: [],
    teams: [],
    developers: [],
    tasks: [],
    workItems: [],
    roles: [],
    users: [],
    permissions: [],
  },

  getters: {
    getUser: state => {
      return state.user;
    },
    getIsLoggedIn: state => {
      return state.isLoggedIn;
    },
    hasPermissions: (state) => (permission) => {
      if (state.user) {
        return state.user.permissions.includes(permission);
      }
      else {
        return false;
      }
    },
    getNavMenuItems: state => {
      return state.navMenuItems;
    },
    getManagers: state => {
      return state.managers;
    },
    getTeams: state => {
      return state.teams;
    },
    getDevelopers: state => {
      return state.developers;
    },
    getTasks: state => {
      return state.tasks;
    },
    getWorkItems: state => {
      return state.workItems;
    },
    getRoles: state => {
      return state.roles;
    },
    getUsers: state => {
      return state.users;
    },
    getPermissions: state => {
      return state.permissions;
    },
  },

  mutations: {
    // setCookies: (state, data) => {
    //   Cookies.set('user', JSON.stringify(data.User), {expires: 7, path: ''});
    //   Cookies.set('isLoggedIn', true, {expires: 7, path: ''});
    // },   // Can use cookies as well doing so so that code does not clash with my other code as cookies names are same. Or can also change names of cookies

    login: (state, data) => {
      state.isLoggedIn = true;
      state.user = data;
    },

    logout: (state, data) => {
      state.isLoggedIn = false;
      state.user = null;
    },

    setUserData: (state, data) => {
      localStorage.setItem('user', JSON.stringify(data.User));
      localStorage.setItem('isLoggedIn', true);
    },

    removeUserData: (state) => {
      localStorage.removeItem('user');
      localStorage.removeItem('isLoggedIn');
    },

    setNavMenuItems: (state) => {
      state.navMenuItems = [];

      state.navMenuItems.push({ title: "Home", route: "home", icon: "fas fa-home" });

      if (state.user.permissions.includes('manager_get')) {
        state.navMenuItems.push({ title: "Managers", route: "manager", icon: "fas fa-user" });
      }
      if (state.user.permissions.includes('teams_get')) {
        state.navMenuItems.push({ title: "Teams", route: "team", icon: "fas fa-users" });
      }
      if (state.user.permissions.includes('work_get')) {
        state.navMenuItems.push({ title: "Work Items", route: "work", icon: "fas fa-file-circle-plus" });
      }
      if (state.user.permissions.includes('developers_get')) {
        state.navMenuItems.push({ title: "Developers", route: "developer", icon: "fas fa-users" });
      }
      if (state.user.permissions.includes('tasks_get')) {
        state.navMenuItems.push({ title: "Tasks", route: "task", icon: "fas fa-list-check" });
      }
      // if (state.user.permissions.includes('teams_get')){
      //   state.navMenuItems.push({ title: "Teams", route: "team", icon: "fas fa-home" });
      // }
      if (state.user.permissions.includes('user_create')) {
        state.navMenuItems.push({ title: "Users", route: "user", icon: "fas fa-user-plus" });
      }
      // if (state.user.permissions.includes('teams_get')){
      //   state.navMenuItems.push({ title: "Teams", route: "team", icon: "fas fa-home" });
      // }
      if (state.user.permissions.includes('work_publish')) {
        state.navMenuItems.push({ title: "Publish Work", route: "publishWork", icon: "fas fa-upload" });
      }
      if (state.user.permissions.includes('approve_work')) {
        state.navMenuItems.push({ title: "Approve Work", route: "approveWork", icon: "fas fa-check-double" });
      }
      if (state.user.permissions.includes('roles_get')) {
        state.navMenuItems.push({ title: "Roles", route: "role", icon: "fas fa-person" });
      }
    },

    setManagers: (state, data) => {
      state.managers = data;
    },

    setTeams: (state, data) => {
      state.teams = data;
    },

    setDevelopers: (state, data) => {
      state.developers = data;
    },

    setTasks: (state, data) => {
      state.tasks = data;
    },

    setWorkItems: (state, data) => {
      state.workItems = data;
    },

    setRoles: (state, data) => {
      state.roles = data;
    },

    setUsers: (state, data) => {
      state.users = data;
    },

    setPermissions: (state, data) => {
      state.permissions = data;
    }
  },

  actions: {
    login: async (context, data) => {
      try {
        const res = await loginApi.post('login/', data);
        if (res.status === 200 && res.data.User) {
          context.commit('login', res.data.User);
          context.commit('setNavMenuItems');
          context.commit('setUserData', res.data);
          return res.data;
        }
      }
      catch (error) {
        console.log(error);
      }
    },

    logout: async (context, data) => {
      try {
        const res = await loginApi.post('logout/');
        if (res.status === 200) {
          context.commit('logout');
          context.commit('removeUserData');
          return res.data;
        }
      }
      catch (error) {
        console.log(error);
      }
    },

    currentUser: async (context) => {
      try {
        const res = await loginApi.get('currentuser/');
        if (res.status === 200 && res.data.User) {
          context.commit('login', res.data.User);
          context.commit('setNavMenuItems');
          return res.data;
        }
      }
      catch (error) {
        console.log(error);
      }
    },

    getManagersData: async (context) => {
      try {
        const res = await backendApi.get('managers/');
        if (res.status === 200) {
          context.commit('setManagers', res.data);
          return res.data;
        }
      }
      catch (error) {
        console.log(error);
      }
    },

    getManagerById: async (context, payload) => {
      try {
        const { id } = payload;
        if (id) {
          const res = await backendApi.get(`managers/${id}/`);
          if (res.status === 200) {
            return res.data;
          }
        }
      }
      catch (error) {
        console.log(error);
      }
    },

    getTeamsData: async (context, manager_id) => {
      let res;
      try {
        if (manager_id) {
          res = await backendApi.get(`teams/?manager=${manager_id}`);
        }
        else {
          res = await backendApi.get(`teams/`);
        }
        if (res.status === 200) {
          context.commit('setTeams', res.data);
          return res.data;
        }
      }
      catch (error) {
        console.log(error);
      }
    },

    getTeamById: async (context, id) => {
      try {
        if (id) {
          const res = await backendApi.get(`teams/${id}/`);
          if (res.status === 200) {
            return res.data;
          }
        }
      }
      catch (error) {
        console.log(error);
      }
    },

    getDevelopersData: async (context) => {
      try {
        const res = await backendApi.get('developers/');
        if (res.status === 200) {
          context.commit('setDevelopers', res.data);
          return res.data;
        }
      }
      catch (error) {
        console.log(error);
      }
    },

    getDeveloperById: async (context, id) => {
      try {
        if(id){
          const res = await backendApi.get(`developers/${id}/`);
          if (res.status === 200) {
            return res.data;
          }
        }
      }
      catch (error) {
        console.log(error);
      }
    },

    getTasksData: async (context) => {
      try {
        const res = await backendApi.get('tasks/');
        if (res.status === 200) {
          context.commit('setTasks', res.data);
          return res.data;
        }
      }
      catch (error) {
        console.log(error);
      }
    },

    getTaskById: async (context, id) => {
      try {
        if (id) {
          const res = await backendApi.get(`tasks/${id}/`);
          if (res.status === 200) {
            return res.data;
          }
        }
      }
      catch (error) {
        console.log(error);
      }
    },

    getWorkItemsData: async (context, payload) => {
      try {
        const { is_approved } = payload;
        const res = await fileApi.get(`workItems/?is_approved=${is_approved}`);
        if (res.status === 200) {
          context.commit('setWorkItems', res.data);
          return res.data;
        }

      }
      catch (error) {
        console.log(error);
      }
    },

    getWorkItemById: async (context, id) => {
      try {
        if(id){
          const res = await fileApi.get(`workItems/${id}/`);
          if (res.status === 200) {
            return res.data;
          }
        }
      }
      catch (error) {
        console.log(error);
      }
    },

    getRolesData: async (context) => {
      try {
        const res = await backendApi.get('roles/');
        if (res.status === 200) {
          context.commit('setRoles', res.data);
          return res.data;
        }
      }
      catch (error) {
        console.log(error);
      }
    },

    getUsersData: async (context) => {
      try {
        const res = await backendApi.get('users/');
        if (res.status === 200) {
          context.commit('setUsers', res.data);
          return res.data;
        }
      }
      catch (error) {
        console.log(error);
      }
    },

    getUserById: async (context, id) => {
      try {
        if(id){
          const res = await backendApi.get(`users/${id}/`);
          if (res.status === 200) {
            return res.data;
          }
        }
      }
      catch (error) {
        console.log(error);
      }
    },

    getPermissionsData: async (context) => {
      try {
        const res = await backendApi.get('permissions/');
        if (res.status === 200) {
          context.commit('setPermissions', res.data);
          return res.data;
        }
      }
      catch (error) {
        console.log(error);
      }
    },

    addWorkItem: async (context, payload) => {
      try {
        const res = await fileApi.post('workItems/', payload);
        if (res.status === 201) {
          console.log("Backend Res", res.data);
          return res.data;
        }
      }
      catch (error) {
        console.log(error);
      }
    },

    editWorkItem: async (context, payload) => {
      const {id} = payload;
      try{
        const res = await fileApi.put(`workItems/${id}/update/`, payload);
        if(res.status === 200){
          return res.data;
        }
      }
      catch(error){
        return error;
      }
    },

    deleteWorkIten: async (context, id) => {
      try{
        const res = await backendApi.delete(`workItems/${id}/delete/`);
        if(res.status === 200){
          return res.data;
        }
      }
      catch (error){
        return error;
      }
    },

    approveWorkItem: async (context, id) => {
      try {
        const res = await backendApi.put(`workItems/${id}/approve/`);
        if (res.status === 200) {
          return res.data;
        }
      }
      catch (error) {
        return error;
      }
    },

    addManager: async (context, payload) => {
      try {
        const res = await backendApi.post('managers/', payload);
        if (res.status === 201) {
          return res.data;
        }
      }
      catch (error) {
        console.log(error);
      }
    },

    editManager: async (context, payload) => {
      const {id} = payload;
      console.log("Here Man", payload, id);
      try{
        const res = await backendApi.put(`managers/${id}/update/`, payload);
        if(res.status === 200){
          return res.data;
        }
      }
      catch (error){
        console.log(error);
        return error;
      }
    },

    deleteManager: async (context, id) => {
      try {
        if (id) {
          const res = await backendApi.delete(`managers/${id}/delete/`);
          if (res.status === 200) {
            return res.data;
          }
        }
      }
      catch (error) {
        console.log(error);
      }
    },

    addRole: async (context, payload) => {
      try {
        const res = await backendApi.post('roles/', payload);
        if (res.status === 201) {
          return res.data;
        }
      }
      catch (error) {
        console.log(error);
      }
    },

    addTeam: async (context, payload) => {
      try {
        const res = await backendApi.post('teams/', payload);
        if (res.status === 201) {
          return res.data;
        }
      }
      catch (error) {
        return error;
      }
    },

    editTeam: async (context, payload) => {
      const {id} = payload;
      try{
        const res = await backendApi.put(`teams/${id}/update/`, payload);
        if(res.status === 200){
          return res.data;
        }
      }
      catch (error){
        return error;
      }
    },

    deleteTeam: async (context, id) => {
      try {
        if (id) {
          const res = await backendApi.delete(`teams/${id}/delete/`);
          if (res.status === 200) {
            return res.data;
          }
        }
      }
      catch (error) {
        return error;
      }
    },

    addDeveloper: async (context, payload) => {
      try {
        const res = await backendApi.post('developers/', payload);
        if (res.status === 201) {
          return res.data;
        }
      }
      catch (error) {
        return error;
      }
    },

    editDeveloper: async (context, payload) => {
      const {id} = payload;
      try{
        const res = await backendApi.put(`developers/${id}/update/`, payload);
        if(res.status === 200){
          return res.data;
        }
      }
      catch (error){
        return error;
      }
    },

    deleteDeveloper: async (context, id) => {
      try {
        if (id) {
          const res = await backendApi.delete(`developers/${id}/delete`);
          if (res.status === 200) {
            return res.data;
          }
        }
      }
      catch (error) {
        return error;
      }
    },

    addTask: async (context, payload) => {
      try {
        const res = await backendApi.post('tasks/', payload);
        if (res.status === 201) {
          return res.data;
        }
      }
      catch (error) {
        console.log(error);
      }
    },

    editTask: async (context, payload) => {
      const {id} = payload;
      try{
        const res = await backendApi.put(`tasks/${id}/update/`, payload);
        if(res.status === 200){
          return res.data;
        }
      }
      catch (error){
        return error
      }
    },

    deleteTask: async (context, id) => {
      try {
        if (id) {
          const res = await backendApi.delete(`tasks/${id}/delete`);
          if (res.status === 200) {
            return res.data;
          }
        }
      }
      catch (error) {
        return error;
      }
    },

    addUser: async (context, payload) => {
      try {
        const res = await backendApi.post('users/', payload);
        if (res.status === 201) {
          return res.data;
        }
      }
      catch (error) {
        return error;
      }
    },

    editUser: async (context, payload) => {
      const {id} = payload;
      try{
        const res = await backendApi.put(`users/${id}/update/`, payload);
        if(res.status === 200){
          return res.data;
        }
      }
      catch (error){
        return error;
      }
    },

    deleteUser: async (context, id) => {
      try {
        if (id) {
          const res = await backendApi.delete(`users/${id}/delete`);
          if (res.status === 200) {
            return res.data;
          }
        }
      }
      catch (error) {
        return error;
      }
    },

    loadUserData: (context, data) => {
      const user = localStorage.getItem('user');
      const isLoggedIn = localStorage.getItem('isLoggedIn');

      if (user && isLoggedIn) {
        context.commit('login', JSON.parse(user));
      }
    },

    // loadCookies: (context, data) => {
    //   const user = Cookies.get('user');
    //   const isLoggedIn = Cookies.get('isLoggedIn');

    //   if(user && isLoggedIn){
    //     context.commit('login', JSON.parse(user));
    //   }
    // }   // Same as above reason

  },
})
