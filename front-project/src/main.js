import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
// 全局配置，src新建config目录，在index.js中配置
import config from '@/config'
import ViewUI from 'view-design';
// import style
import 'view-design/dist/styles/iview.css';
Vue.use(ViewUI);

Vue.config.productionTip = false;
Vue.prototype.$config = config;
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");