import Vue from "vue";
import VueRouter from "vue-router";
import routes from "./routes";
Vue.use(VueRouter);

// configure router
const router = new VueRouter({
  routes, // short for routes: routes
  linkActiveClass: "active",
  mode: 'history',
});


router.beforeEach((to, from, next) => {
  let role = localStorage.getItem('role');
  let token = localStorage.getItem('token');
  
  // 如果有token并且试图进入login，则跳转到自己角色对应的dashboard
  if (token && to.path === '/login') {
    next(`/dashboard/${role}`);
  } else if (!token && to.path !== '/login') {
    // 如果没有token且试图进入除了login之外的页面，跳转到登录页
    next('/login');
  } else if (token && to.path.includes(role)) {
    // 如果有token且试图进入的页面路径包含自己的角色，那么可以访问
    next();
  } else if (token) {
    // 如果有token且试图进入的页面路径不包含自己的角色，那么跳转到自己角色对应的dashboard
    next(`/dashboard/${role}`);
  } else {
    // 其他情况，如登录页和没有token的情况，直接访问
    next();
  }
});


export default router;
