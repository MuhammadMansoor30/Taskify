import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import store from '@/store'

const routes = [
  {
    path: '/',
    name: 'login',
    meta: {title: 'Login'},
    component: LoginView
  },
  {
    path: '/home',
    name: 'home',
    meta: {title: 'Home'},
    component: HomeView
  },
  {
    path: '/manager',
    name: 'manager',
    meta: {title: 'Managers'},
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/ManagerView.vue')
  },
  {
    path: '/team',
    name: 'team',
    meta: {title: 'Teams'},
    component: () => import('../views/TeamsView.vue'),
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.name !== 'login' && !store.getters.getIsLoggedIn) {
    next({ name: 'login' });
  } else {
    next();
  }
});

export default router
