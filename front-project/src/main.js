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

Vue.config.productionTip = false;
Vue.prototype.$config = config;

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