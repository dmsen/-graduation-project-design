<template>
  <Layout style="height: 100%" class="main">
    <Sider
      hide-trigger
      collapsible
      :width="220"
      :collapsed-width="64"
      v-model="collapsed"
      class="left-sider"
      :style="{ overflow: 'hidden' }"
    >
      <side-menu
        accordion
        ref="sideMenu"
        :active-name="$route.name"
        :collapsed="collapsed"
        @on-select="turnToPage"
        :menu-list="menuList"
      >
        <div class="logo-con">
          <!-- <img
            v-show="!collapsed"
            :src="maxLogo"
            key="max-logo"
            style="width: 200px;height: 75px;margin-top: -6px"
          />-->
          <img v-show="collapsed" :src="minLogo" key="min-logo" />
        </div>
      </side-menu>
    </Sider>

    <Layout>
      <Header class="header-con">
        <header-bar :collapsed="collapsed" @on-coll-change="handleCollapsedChange">
          <user :user-avatar="userAvatar" />
          <!-- <img
            style="height: 80px;width:300px;margin-top: 0;margin-right: 10px"
            src="../../assets/pic/lin_max_log.png"
          />-->
        </header-bar>
      </Header>
      <Content class="main-content-con">
        <Layout class="main-layout-con">
          <div class="tag-nav-wrapper"></div>
          <Content class="content-wrapper">
            <!-- <keep-alive :include="cacheList">
              <router-view />
            </keep-alive>-->
            <keep-alive>
              <router-view />
            </keep-alive>
            <ABackTop :height="100" :bottom="80" :right="50" container=".content-wrapper"></ABackTop>
          </Content>
        </Layout>
      </Content>
    </Layout>
  </Layout>
</template>

<script>
import minLogo from "@/assets/pic/lin.png";
import maxLogo from "@/assets/pic/lin_max_log.png";
import SideMenu from "./components/side-menu";
import User from "./components/user";
import ABackTop from "./components/a-back-top";
import HeaderBar from "./components/header-bar";
import "./mymain.less";
import { mapMutations, mapActions, mapGetters } from "vuex";
export default {
  name: "myMain",
  components: {
    SideMenu,
    User,
    ABackTop,
    HeaderBar
  },
  data() {
    return {
      collapsed: localStorage.getItem("collapseLand") == "true" ? true : false,
      minLogo,
      maxLogo
    };
  },
  computed: {
    menuList() {
      return this.$store.getters.menuList;
    },
    userAvatar() {
      return "http://www.dmsen.cn/static/ali_index_files/img/pic2.jpg";
      // return  ("http://127.0.0.1:8000/media/" + this.$store.state.user.avatorImgPath);
    }
  },
  watch: {
    $route(newRoute) {
      const { name, query, params, meta } = newRoute;
      this.setBreadCrumb(newRoute);
      this.$refs.sideMenu.updateOpenName(newRoute.name);
    },
    collapsed(val, newVal) {
      localStorage.setItem("collapseLand", !newVal);
    }
  },
  methods: {
    ...mapMutations(["setBreadCrumb", "setLocal"]),
    turnToPage(route) {
      let { name, params, query } = {};
      if (typeof route === "string") name = route;
      else {
        name = route.name;
        params = route.params;
        query = route.query;
      }
      if (name.indexOf("isTurnByHref_") > -1) {
        window.open(name.split("_")[1]);
        return;
      }
      this.$router.push({
        name,
        params,
        query
      });
    },

    handleCollapsedChange(state) {
      this.collapsed = state;
    }
  },
  mounted() {
    /**
     * @description 初始化设置面包屑导航和标签导航
     */
    console.log(this.$route);
    this.setBreadCrumb(this.$route);
  }
};
</script>


