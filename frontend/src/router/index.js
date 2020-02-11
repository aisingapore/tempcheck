import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import Home from '@/pages/Home'
import NewEntry from '@/pages/NewEntry'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Hello',
      component: Hello
    },
    {
      path: '/home',
      name: 'Home',
      component: Home
    },
    {
      path: '/entries/new',
      name: 'NewEntry',
      component: NewEntry
    }
  ]
})
