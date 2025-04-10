import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/Home.vue'),
    redirect: '/users',
    children: [
      {
        path: '/users',
        name: 'Users',
        component: () => import('@/view/users.vue'),
        meta: {
          title: '用户管理'
        }
      },
      {
      
        path: '/redis',
        name: 'Redis',
        component: () => import('@/view/redis.vue'),
        meta: {
          title: 'Redis'
        }
      }
      

    ]
    
    
  }

];

const router = createRouter({
  history: createWebHistory(),
  routes
});

 export default router;