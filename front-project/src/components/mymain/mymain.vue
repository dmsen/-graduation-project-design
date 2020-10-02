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
        <Modal v-model="badgeModal" title="通知" width="600px">
          <div
            style="width: 600px;margin-left: 250px;font-weight: bold;font-size: 15px"
            v-show="noticeNone"
          >
            暂无通知
          </div>
          <div v-show="noticeHave">
            <!--<Card v-for="(item,i) in noticeItem" :key=i>-->
            <!--用户名{{item.byPerson}}: 内容{{item.content}}:时间{{formateDate(item.time)}}-->
            <!---->
            <!--</Card>-->
            <Collapse accordion>
              <Panel
                v-for="(item, i) in noticeItem"
                :key="i"
                :hide-arrow="true"
              >
                <span style="font-weight: bold"
                  >用户名：{{ item.byPerson }} </span
                ><span style="float: right">{{ formateDate(item.time) }}</span>
                <!--<p slot="content">{{item.content}}</p>-->
                <div slot="content" style="margin-bottom: 5px">
                  <p style="word-break: break-all">
                    {{ item.content }}
                    <Button
                      style="float: right;margin-right: -15px;"
                      @click="readNotice(item.linSystemNoticeId)"
                      >标记已读</Button
                    >
                  </p>
                </div>
              </Panel>
            </Collapse>
            <Row style="margin-top: 16px">
              <Col span="24">
                <Button type="primary" @click="readEdNotice">
                  查看已读消息</Button
                >
                <Button
                  type="primary"
                  @click="getNoticeFuntion"
                  style="margin-left: 10px"
                >
                  查看未读消息</Button
                >
                <Page
                  :total="dataLength"
                  :current="currentPages"
                  size="small"
                  show-elevator
                  :page-size="3"
                  @on-change="changePages"
                  show-total
                  style="float: right;margin-top: 10px"
                />
              </Col>
              <!--<Col span = "10" offset = "3"   >-->
              <!--<Page :total="dataLength" :current="currentPages" size="small" show-elevator  :page-size ="3" @on-change="changePages" show-total/>-->
              <!--</Col>-->
            </Row>
          </div>

          <div slot="footer">
            <span style="margin-right: 12px">若有问题请联系管理员</span>
          </div>
        </Modal>
        <header-bar
          :collapsed="collapsed"
          @on-coll-change="handleCollapsedChange"
        >
          <Badge :offset="bOffset" overflow-count="99" :count="badgeCount">
            <a href="#" @click="showBadgeModal">
              <Icon type="ios-notifications-outline" size="26"></Icon
            ></a>
          </Badge>
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
            <keep-alive>
              <router-view />
            </keep-alive>
            <ABackTop
              :height="100"
              :bottom="80"
              :right="50"
              container=".content-wrapper"
            ></ABackTop>
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
    HeaderBar,
  },
  data() {
    return {
      collapsed: localStorage.getItem("collapseLand") == "true" ? true : false,
      minLogo,
      maxLogo,
      badgeModal: false,
      badgeCount: 0,
      bOffset: [15, -5],
      noticeItem: null,
      noticeNone: false,
      noticeHave: false,
      dataLength: 0,
      currentPages: 1,
    };
  },
  computed: {
    menuList() {
      return this.$store.getters.menuList;
    },
    userAvatar() {
      // return "http://www.dmsen.cn/static/ali_index_files/img/pic2.jpg";
      if (localStorage.getItem("avatorImgPath"))
        return (
          this.$config.baseUrl.mediaPath + localStorage.getItem("avatorImgPath")
        );
      else return "http://www.dmsen.cn/static/ali_index_files/img/pic2.jpg";
    },
  },
  watch: {
    $route(newRoute) {
      const { name, query, params, meta } = newRoute;
      this.setBreadCrumb(newRoute);
      this.$refs.sideMenu.updateOpenName(newRoute.name);
    },
    collapsed(val, newVal) {
      localStorage.setItem("collapseLand", !newVal);
    },
  },
  methods: {
    ...mapMutations(["setBreadCrumb", "setLocal"]),
    ...mapActions(["handGetNotice", "handReadNotice", "handReadEdNotice"]),
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
        query,
      });
    },

    handleCollapsedChange(state) {
      this.collapsed = state;
    },
    showBadgeModal() {
      let that = this;
      if (that.noticeItem === null) {
        that.noticeNone = true;
        that.badgeModal = true;
        that.noticeHave = false;
      } else {
        that.badgeModal = true;
        that.noticeNone = false;
        that.noticeHave = true;
        that.getNoticeFuntion();
      }
    },
    // 获取用户通知
    async getNoticeFuntion() {
      const _this = this;
      const sendPage = this.currentPages;
      _this.noticeItem = null;
      try {
        const userId = localStorage.getItem("userId");
        const Res = await _this.handGetNotice({ userId, sendPage });
        console.log(Res);
        if (Res.result === 1) {
          _this.badgeCount = 0;
        } else {
          _this.noticeItem = Res.msg;
          _this.badgeCount = Res.allDateLength;
          _this.dataLength = Res.allDateLength;
        }
      } catch (err) {
        _this.$Message.error("未知错误" + err);
      }
    },
    // 标记通知已读
    async readNotice(id) {
      const _this = this;
      try {
        console.log(id);
        console.log("__________________");
        const Res = await _this.handReadNotice({ id });
        console.log(Res);
        if (Res.result === 1) {
          _this.$Message.error("发生错误，请稍后再试");
        } else {
          _this.$Message.success("操作成功");
          _this.getNoticeFuntion();
        }
      } catch (err) {
        _this.$Message.error("未知错误" + err);
      }
    },
    // 获取已读通知
    async readEdNotice() {
      const _this = this;
      const sendPage = this.currentPages;
      _this.noticeItem = null;
      try {
        const userId = _this.$store.state.user.userId;
        const Res = await _this.handReadEdNotice({ userId, sendPage });
        console.log(Res);
        if (Res.result === 1) {
          _this.badgeCount = 0;
        } else {
          _this.noticeItem = Res.msg;
          _this.badgeCount = Res.allDateLength;
          _this.dataLength = Res.allDateLength;
        }
      } catch (err) {
        _this.$Message.error("未知错误" + err);
      }
    },
    changePages(val) {
      this.currentPages = val;
      this.getNoticeFuntion();
    },
    /**
     * 时间格式化，将时间格式转成字符串
     */
    formateDate(datetime) {
      // let  = "2019-11-06T16:00:00.000Z"
      function addDateZero(num) {
        return num < 10 ? "0" + num : num;
      }
      let d = new Date(datetime);
      let formatdatetime =
        d.getFullYear() +
        "-" +
        addDateZero(d.getMonth() + 1) +
        "-" +
        addDateZero(d.getDate()) +
        " " +
        addDateZero(d.getHours()) +
        ":" +
        addDateZero(d.getMinutes()) +
        ":" +
        addDateZero(d.getSeconds());
      return formatdatetime;
    },
  },
  mounted() {
    /**
     * @description 初始化设置面包屑导航和标签导航
     */
    console.log(this.$route);
    this.setBreadCrumb(this.$route);
    // 获取通知
    this.getNoticeFuntion();
  },
};
</script>
