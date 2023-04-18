import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'

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
    // {
    //   path: '/add-to-slack',
    //   name: 'add-to-slack',
    //   component: AddToSlackView
    // },
    // {
    //   path: '/how-to-use',
    //   name: 'how-to-use',
    //   component: HowToUseView
    // },
    // {
    //   path: '/how-to-use',
    //   name: 'how-to-use',
    //   component: HowToUseView
    // },
    // {
    //   path: '/use-cases',
    //   name: 'use-cases',
    //   component: UseCasesView
    // },
    // {
    //   path: '/use-cases',
    //   name: 'use-cases',
    //   component: UseCasesView
    // },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    // {
    //   path: '/terms-and-conditions',
    //   name: 'terms-and-conditions',
    //   component: TermsAndConditionsView
    // },
    // {
    //   path: '/privacy-policy',
    //   name: 'privacy-policy',
    //   component: PrivacyPolicyView
    // },
  ]
})

export default router
