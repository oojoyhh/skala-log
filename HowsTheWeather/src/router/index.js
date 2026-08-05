import { createRouter, createWebHistory } from 'vue-router'
import WeatherHomeView from '../views/WeatherHomeView.vue'

const routes = [
  {
    path: '/',
    name: 'WeatherHome',
    component: WeatherHomeView,
  },
  {
    path: '/about',
    name: 'WeatherAbout',
    component: () => import('../views/TunedAboutView.vue'),
  },
  {
    path: '/exercises',
    name: 'Exercises',
    component: () => import('../views/ExercisesView.vue'),
  },
  {
    path: '/cities',
    name: 'CitySearch',
    component: () => import('../views/CitySearchView.vue'),
  },
  {
    path: '/forecast',
    name: 'WeatherForecast',
    component: () => import('../views/WeatherForecastView.vue'),
  },
  {
    path: '/weather/:cityId',
    name: 'WeatherDetail',
    component: () => import('../views/WeatherDetailView.vue'),
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFoundView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      }
    }

    return { top: 0 }
  },
})

export default router
