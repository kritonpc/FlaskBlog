import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Category from '../components/Category.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { title: 'Saidit' }
  },
  {
    path: '/profile',
    name: 'Profile',
    meta: { title: 'Saidit - Profile' },
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/Profile.vue')
  },
  {
    path: "/categories/:category",
    component: Category,
    props: true,
    meta: { title: 'Saidit' }
  },
  // login and register routes
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { title: 'Saidit' }
  },
  {
    path: '/logout',
    name: 'Logout',
    component: () => import('../views/Logout.vue'),
    meta: { title: 'Saidit' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
    meta: { title: 'Saidit' }
  },
  {
    path: '/admin',
    name: 'Admin Panel',
    component: () => import('../views/Admin.vue'),
    meta: { title: 'Saidit' }
  },
]

const router = new VueRouter({
  routes
})

export default router
