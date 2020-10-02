<template>
  <div>
    <Row>
      <Col span="18">
        <Row style="margin-top: 16px">
          <Col span="5"> </Col>
          <Col span="13" offset="10" style="text-align: right">
            <Page
              :total="dataLength"
              :current="currentPages"
              size="small"
              show-elevator
              :page-size="10"
              @on-change="changePages"
              show-total
            />
          </Col>
        </Row>

        <Card v-for="i in 10" :key="i">
          <p slot="title" style="height: 20px">
            <Icon type="ios-film-outline"></Icon>
            <span style="font-size: 20px">测试</span>
          </p>
          <Rate show-text allow-half v-model="valueText" disabled slot="extra">
            评分：<span style="color: #f5a623">{{ valueText }}</span>
          </Rate>
          <Row :gutter="16">
            <Col span="2">
              <figure>
                <img
                  src="http://www.dmsen.cn/static/ali_index_files/img/pic2.jpg"
                  alt="头像"
                  width="100%"
                />
                <figcaption style="text-align: center">
                  lin
                </figcaption>
              </figure>
              <!--<Img src="http://www.dmsen.cn/static/ali_index_files/img/pic2.jpg" style="width: 20%" title="用户头像"/>-->
              <!--<span style="display: block;margin-top:50px;position: absolute;margin-left: -20px;">用户名</span>-->
            </Col>
            <Col span="18">
              内容
            </Col>
          </Row>

          <Row style="margin-top: 10px">
            <Divider style="margin: 5px 0" />
            <Col span="6">
              14点31分
              <!-- {{ formateDate(item.courseEvaluateDate) }} -->
            </Col>
            <Col span="6" :offset="12">
              暂定
            </Col>
          </Row>
        </Card>
      </Col>

      <Col span="6">
        <Card style="">
          <p slot="title">
            <Icon type="ios-film-outline"></Icon>
            最新公告
          </p>
          <a href="http://www.dmsen.cn" slot="extra">
            <Icon type="ios-loop-strong"></Icon>
            前往 作者 主页
          </a>
          <p style="color: red">
            因此项目为软件工程课设，此系统暂停更新【除非另有需求】
          </p>
        </Card>
        <Card style="height: 255px;">
          <p slot="title">
            <Icon type="ios-film-outline"></Icon>
            技术概要
          </p>
          <a href="https://github.com/dmsen" slot="extra">
            <Icon type="ios-loop-strong"></Icon>
            前往 作者 github
          </a>
          <p>
            <span class="spanStyle">前端涉及到的知识：</span
            >【vue相关（router、vuex）、组件库（iview，element-ui）、框架（iview-admin）】
          </p>
          <p>
            <span class="spanStyle">涉及后端相关知识：</span
            >【语言（python）、框架（django）】
          </p>
          <p><span class="spanStyle">web服务器：</span>【nginx】</p>
          <p>
            <span class="spanStyle">web框架：</span
            >【django（利用gunicorn来启动wsgi）】
          </p>
        </Card>
        <Card style="height: 205px;">
          <p slot="title">
            <Icon type="ios-film-outline"></Icon>
            相关功能
          </p>
          <a href="#" slot="extra" @click.prevent="changeLimit">
            <Icon type="ios-loop-strong"></Icon>
            查看本系统开发前的需求文档
          </a>
          <p>
            <span class="spanStyle">用户：</span
            >【登陆、注册、权限验证、修改头像、更新个人信息、删除】
          </p>
          <p><span class="spanStyle">课程管理：</span>【增删改查】</p>
          <p><span class="spanStyle">课程评价：</span>【增、查】</p>
          <p><span class="spanStyle">用户通知：</span>【增、查】</p>
          <p><span class="spanStyle">数据库:</span>【六表】</p>
        </Card>
      </Col>
    </Row>
  </div>
</template>

<script>
// import { handGetEvl } from "@/api/course.js";
export default {
  name: "home",
  components: {},
  data() {
    return {
      dataLength: 0,
      currentPages: 1,
      evalItem: null,
      valueText: 3.9
    };
  },
  methods: {
    changePages(val) {
      this.currentPages = val;
      // 重新获取分页后的数据
      this.getEva();
    },
    formateDate(datetime) {
      // let  = "2019-11-06T16:00:00.000Z"
      function addDateZero(num) {
        return num < 10 ? "0" + num : num;
      }
      // let d = new Date(datetime);
      let d = new Date(Date.parse(datetime) - 8 * 60 * 60 * 1000);
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
    async getEva() {
      //  获取数据
    }
  },
  beforeMount() {},
  mounted() {
    // 获取最新数据
    // this.getEva();
  }
};
</script>

<style scoped>
.spanStyle {
  font-weight: bold;
  color: #348eed;
}
</style>