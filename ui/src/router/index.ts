import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import AddToSlackView from '../views/AddToSlackView.vue'
import HowToUseView from "../views/HowToUseView.vue";
import UseCasesView from "../views/UseCasesView.vue";
import AboutView from "../views/AboutView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/add-to-slack',
      name: 'add-to-slack',
      component: AddToSlackView
    },
    {
      path: '/how-to-use',
      name: 'how-to-use',
      component: HowToUseView
    },
    {
      path: '/use-cases',
      name: 'use-cases',
      component: UseCasesView
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    },
    {
      path: '/terms-and-conditions',
      name: 'terms-and-conditions',
      component: () => import('../views/TermsAndConditionsView.vue')
    },
    {
      path: '/after-add-to-slack',
      name: 'after-add-to-slack',
      component: () => import('../views/AfterAddToSlack.vue')
    },
  ]
})

export default router
