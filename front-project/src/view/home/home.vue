<template>
  <div>
    <Row>
      <Col span="18">
        <Card v-for="i in 4" :key="i" >
          <p slot="title" style="height: 20px">
            <Row>
              <Col span="4">
                <Icon type="ios-film-outline"></Icon>
                <span style="font-size: 20px">标题</span>    
              </Col>
              <Col span="20" style="text-align: right;">
                <Poptip trigger="hover" content="阅读量" placement="left">
                  <Icon type="md-eye" size="22" /> 11222121
                </Poptip>
                <Poptip trigger="hover" content="点赞数" placement="left">
                  <Icon type="md-flame" size="22" />121212121
                </Poptip>
              </Col>
            </Row>
          </p>   
          <!-- <Rate show-text allow-half v-model="valueText" disabled slot="extra">
            评分：<span style="color: #f5a623">{{ valueText }}</span>
          </Rate> -->
          <Row :gutter="16">
            <Col span="2">
              <figure>
                <img
                  src="http://www.dmsen.cn/static/ali_index_files/img/pic2.jpg"
                  alt="头像"
                  height="70%"
                  width="70%"
                />
                <figcaption style="text-align: center;margin-left: 5px;width: 60px;height: 20px;overflow: hidden;">
                  lin1linlin1lin lin lin lin lin
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
            <Col span="6" style="font-size: 8px;text-align: left;margin-top: 10px;">
              2020-11-03 16:47:42
              <!-- {{ formateDate(item.courseEvaluateDate) }} -->
            </Col>
            <Col span="12" offset="6" style="text-align: right;overflow: hidden;">
              <Button type="info" v-for="i in 5" :key="i" ghost size="small" style="margin-right: 10px;margin-top: 10px;">InfoInfo{{i}}</Button>
             
            </Col>
          </Row>
        </Card>
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
            此项目为毕业系统设计
          </p>
        </Card>
        <Card>
           <p slot="title">
            <Row>
              <Col span="2"> 
                榜单
              </Col> 
              <Col span="7" offset="15" style="text-indent: 8px;">热度<Divider type="vertical" />发帖数</Col>
            </Row>
          </p> 
         
          <Row v-for="i in 5" :key="i">
                <Col span="2">
              <Button
                type="primary"
                shape="circle"
                style="width:4px;margin-left:-6px;padding-left:10px;"
                >{{ i }}</Button
              ></Col
            >
            <Col span="15">
              <Avatar :src="userAvatar" /><span>asd123</span></Col
            >
            <Col span="3" >
              <Poptip trigger="hover" content="热度" placement="right"
                ><Button style="margin-right:10px">112</Button></Poptip
              ></Col
            >
            <Col span="3" style="margin-left: 5px;">
              <Poptip trigger="hover" content="发帖数" placement="right"
                ><Button style="margin-right:10px">222</Button></Poptip
              ></Col
            >
            <Divider style="margin-top:15px"></Divider>
          </Row>
        </Card>
        <Card style="">
          <p slot="title">
            <Icon type="ios-film-outline"></Icon>
            最近活跃
          </p>
        <Row v-for="i in 3" :key="i">
          <Col span="3"><Avatar :src="userAvatar" /></Col>
          <Col span="14" style="font-weight: bold;overflow: hidden;"><a href="">标题标题标题标题标题标题标题标题</a></Col>
          <Col span="7" style="font-size: 8px;text-align: right;">2020-11-03 16:47:42</Col>
          <Divider style="margin:10px"></Divider>
        </Row>
        </Card>
        <Card>
          <p slot="title">
            <Icon type="ios-film-outline"></Icon>
           热门标签
          </p>
          <!-- <a href="https://github.com/dmsen" slot="extra">
            <Icon type="ios-loop-strong"></Icon>
            前往 作者 github
          </a> -->
          <Tag v-for="i in 10" :key="i" type="border"  color="success" style="margin-left: 15px;margin-bottom: 15px;">标签{{i}}</Tag>
          <!-- <Card v-for="i in 5" :key="i">
            <p><span class="spanStyle">课程管理：</span>【增删改查】</p>
          </Card> -->
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