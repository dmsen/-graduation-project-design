import Vue from "vue";
import config from '@/config'
const {
  homeName
} = config
import VueRouter from "vue-router";
import store from '@/store'
import routes from './routers'
import {
  setToken,
  getToken,
  canTurnTo,
} from '@/libs/myutil'
import iView from 'iview'
Vue.use(VueRouter);

const router = new VueRouter({
  mode: "history",
  routes
});

const turnTo = (to, access, next) => {
  if (canTurnTo(to.name, access, routes)) next() // 有权限，可访问
  else next({
    replace: true,
    name: 'error_401'
  }) // 无权限，重定向到401页面
}
const LOGIN_PAGE_NAME = 'login'
// 路由守卫
router.beforeEach((to, from, next) => {
  console.log("路由信息")
  console.log(to, from, next)
  iView.LoadingBar.start() //iview 中的进度条组件
  const token = getToken() //获取登陆的权限，决定哪些页面可以显示、访问
  if (!token && to.name !== LOGIN_PAGE_NAME) {
    // 未登录且要跳转的页面不是登录页
    next({
      name: LOGIN_PAGE_NAME // 跳转到登录页
    })
  } else if (!token && to.name === LOGIN_PAGE_NAME) {
    // 未登陆且要跳转的页面是登录页
    next() // 跳转
  } else if (token && to.name === LOGIN_PAGE_NAME) {
    // 已登录且要跳转的页面是登录页
    next({
      name: homeName // 跳转到homeName页
    })
  } else {
    if (store.state.user.hasGetInfo) {
      console.log('store.state.user.hasGetInfo  ' + store.state.user.hasGetInfo)
      turnTo(to, store.state.user.access, next)
    } else {
      store.dispatch('getUserInfo').then(user => {
        // 拉取用户信息，通过用户权限和跳转的页面的name来判断是否有权限访问;access必须是一个数组，如：['super_admin'] ['super_admin', 'admin']
        turnTo(to, user.access, next)
        console.log("当前用户权限")
        console.log(user.access, typeof (user.access))
      }).catch((e) => {
        // console.log(e)
        setToken('')
        next({
          name: 'login'
        })
      })
    }
  }
})

router.afterEach(to => {
  // setTitle(to, router.app)
  iView.LoadingBar.finish()
  window.scrollTo(0, 0)
})
export default router;