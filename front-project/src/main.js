import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
// 全局配置，src新建config目录，在index.js中配置
import config from "@/config";
import ViewUI from "view-design";
// import style
import "view-design/dist/styles/iview.css";
Vue.use(ViewUI);

// import "./theme/blue.less";
const theme = localStorage.getItem("themeStyle");
if (theme) {
  import("./theme/" + localStorage.themeStyle + ".less");
} else {
  import("./theme/blue.less");
}

// 树状图
import OrgTree from 'v-org-tree'
import 'v-org-tree/dist/v-org-tree.css'
Vue.use(OrgTree)

// 树状表
import TreeTable from 'tree-table-vue'
Vue.use(TreeTable)
// 导入echarts
import echarts from 'echarts'
// 视频播放器
import Video from 'video.js'
import 'video.js/dist/video-js.css'
// ElementUI
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(ElementUI);


// import Axios from 'axios'
// //axios全局配置
// Vue.prototype.$axios = Axios
// Axios.defaults.baseURL = config.baseUrl.pro
// Axios.defaults.headers.post['Content-Type'] = 'application/json';
// Vue.config.productionTip = false
// vue全局配置
Vue.config.productionTip = false;
Vue.prototype.$config = config;
Vue.prototype.$echarts = echarts;
// 解决页面刷新，vuex数据丢失的问题
//刷新保存状态
if (sessionStorage.getItem("store")) {
  store.replaceState(
    Object.assign({}, store.state, JSON.parse(sessionStorage.getItem("store")))
  );
  sessionStorage.removeItem("store");
}

//监听，在页面刷新时将vuex里的信息保存到sessionStorage里
window.addEventListener("beforeunload", () => {
  sessionStorage.setItem("store", JSON.stringify(store.state));
});



new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");