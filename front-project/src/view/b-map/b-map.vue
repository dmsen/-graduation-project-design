<template>
  <el-container>
    <el-aside style="margin-top:20px;width:320px">
      <Input
        v-model="searchValue"
        placeholder="请输入机构名称"
        style="margin-left: 1px;width:79%"
        clearable
        @on-clear="clearFunction"
      />
      <Button type="primary" style="float: right" @click="searchFunction"
        >搜索</Button
      >
      <el-table
        :data="buildinglist"
        @row-click="skiptomap"
        fit
        highlight-current-row
        stripe
        border
      >
        <el-table-column prop="name" lable="name" align="left" label="热度排名">
          <template slot-scope="scope" align=" left">
            <p style="font-weight: bold">
              {{ scope.row.name }}
              <span style="float: right;margin-right: 10px">
                <Poptip trigger="hover" content="阅读量" placement="left">
                  <Icon type="md-eye" size="22" /> </Poptip
                >{{ scope.row.mapPointViews }}
              </span>
              <span style="float: right">
                <Poptip trigger="hover" content="点赞数" placement="left">
                  <Icon type="md-flame" size="22" />
                </Poptip>
                {{ scope.row.mapPointfare }}
              </span>
            </p>
          </template>
        </el-table-column>
      </el-table>

      <p style="text-align: right;margin-top: 20px">
        <Button
          type="primary"
          style="float: left;margin-top: -5px"
          @click="uploadPoint()"
          >上传</Button
        >
        <Page
          :total="dataLength"
          :current="currentPages"
          size="small"
          show-elevator
          :page-size="6"
          @on-change="changePages"
          show-total
        />
      </p>
    </el-aside>
    <el-container
      id="newmap"
      style="margin-top:20px;margin-left:20px; height:1000px;"
    ></el-container
    >>
    <Button @click="zoomOut()" style="position: absolute;top: 160px;right: 20px"
      >放大</Button
    >
    <Button @click="zoomIn()" style="position: absolute;top: 195px;right: 20px"
      >缩小</Button
    >
    <Button
      @click="resetZoom()"
      style="position: absolute;top: 240px;right: 20px"
      >重置</Button
    >
    <Modal v-model="uploadModal" title="上传机构信息" width="900px">
      <Form :model="formItem" ref="formItem" :label-width="80" class="form">
        <Row>
          <Col span="12">
            <FormItem label="机构名">
              <Input
                prefix="ios-person"
                v-model="formItem.mapPointName"
                style="width: auto"
                clearable
              />
            </FormItem>
            <FormItem label="经度">
              <Input
                prefix="ios-contacts"
                v-model="formItem.mapPointJ"
                style="width: auto"
                placeholder="例子：113.114149"
                clearable
              />
            </FormItem>
            <FormItem label="纬度">
              <Input
                prefix="ios-contacts"
                v-model="formItem.mapPointW"
                style="width: auto"
                placeholder="例子：27.823866"
                clearable
              />
            </FormItem>
            <FormItem label="地址">
              <Input
                prefix="ios-person"
                v-model="formItem.mapPointAddr"
                style="width: auto"
                clearable
              />
            </FormItem>
            <FormItem label="联系电话">
              <Input
                prefix="ios-contacts"
                v-model="formItem.mapPointTel"
                style="width: auto"
                clearable
              />
            </FormItem>
            <FormItem label="床位">
              <Input
                prefix="ios-contacts"
                v-model="formItem.mapPointBedNum"
                style="width: auto"
                clearable
              />
            </FormItem>
            <FormItem label="费用">
              <Input
                prefix="ios-contacts"
                v-model="formItem.mapPointFee"
                style="width: auto"
                clearable
              />
            </FormItem>
          </Col>
          <Col span="12">
            <FormItem label="简介" style="margin-left: -40px">
              <Input
                prefix="ios-contacts"
                v-model="formItem.mapPointJian"
                style="width:360px"
                maxlength="150"
                show-word-limit
                type="textarea"
                :rows="6"
              />
            </FormItem>
            <FormItem label="服务详情" style="margin-left: -40px">
              <Input
                prefix="ios-contacts"
                v-model="formItem.mapPointServer"
                style="width:360px;"
                maxlength="300"
                show-word-limit
                type="textarea"
                :rows="10"
              />
            </FormItem>
          </Col>
        </Row>
      </Form>

      <div slot="footer">
        <Button type="primary" @click="handleSubmit">确认提交</Button>
        <Button type="default" @click="handleCancel">取消</Button>
      </div>
    </Modal>
  </el-container>
</template>

<script>
import {
  mapPointGet,
  mapPointSearch,
  addPointInfo,
  mapPointView
} from "@/api/mapPoint.js";
import VueAplayer from "vue-aplayer";
import config from "@/config";
const mediaUrl = config.baseUrl.mediaPath;
export default {
  components: {
    //别忘了引入组件
    "a-player": VueAplayer
  },
  data() {
    let that = this;
    return {
      formItem: {
        mapPointName: "",
        mapPointJ: "",
        mapPointW: "",
        mapPointAddr: "",
        mapPointTel: "",
        mapPointBedNum: "",
        mapPointFee: "",
        mapPointJian: "",
        mapPointServer: ""
      },
      searchValue: "",
      tabPages: "1",
      dataLength: 0,
      currentPages: 1,
      uploadModal: false,
      //定义指定地点的名称和经纬度
      buildinglist: [
        {
          id: 1,
          name: "湖南工业大学新校区",
          j: 113.114149,
          w: 27.823866,
          addr: "泰山西路88号",
          tel: "(0731)22183311",
          grade: 3
        },
        {
          id: 2,
          name: "中心广场",
          j: 113.159473,
          w: 27.845592,
          addr: "地址：湖南省株洲市芦淞区纺织路27号",
          tel: "",
          grade: 2
        }
      ],
      jd: 113.114149, //初始地图中心点的经纬度
      wd: 27.823866,
      map: {},
      point: {},
      recentItem: null,
      fclickMarker: null,
      lclickMarker: null,
      currentSize: 15,
      step: 1,
      maxSize: 30,
      minSize: 0,
      points: new BMap.Point(113.114149, 27.823866),
      currentMapPoint: 0,
      currentMapPointId: null,
      currentMapPointName: null
    };
  },
  methods: {
    zoomOut() {
      this.currentSize =
        this.currentSize + this.step > this.maxSize
          ? this.currentSize
          : this.currentSize + this.step;
      console.log(this.point);
      if (this.point !== {}) {
        let poi = new BMap.Point(this.point.lng, this.point.lat);
        this.map.centerAndZoom(poi, this.currentSize);
      } else {
        this.map.centerAndZoom(this.points, this.currentSize);
      }
    },
    zoomIn() {
      this.currentSize =
        this.currentSize - this.step < this.minSize
          ? this.currentSize
          : this.currentSize - this.step;
      console.log(this.point);
      if (this.point !== {}) {
        let poi = new BMap.Point(this.point.lng, this.point.lat);
        this.map.centerAndZoom(poi, this.currentSize);
      } else {
        this.map.centerAndZoom(this.points, this.currentSize);
      }
    },
    resetZoom() {
      if (this.point !== {}) {
        let poi = new BMap.Point(this.point.lng, this.point.lat);
        this.map.centerAndZoom(poi, 15);
      } else {
        this.map.centerAndZoom(this.points, 15);
      }
    },
    playVedio() {
      this.$video("player").play();
    },
    pauseVedio() {
      this.$video("player").pause();
      // videojs("player").src("//vjs.zencdn.net/v/oceans.mp4")
      // Document.querySelector('video').pause();
    },
    changePages(val) {
      this.currentPages = val;
      this.getMapPoint();
    },
    loadmap(jd, wd) {
      var _this = this; //保存此时的this值！！！
      this.map = new BMap.Map("newmap"); // 创建地图实例

      var ctrl_nav = new BMap.NavigationControl({
        anchor: BMAP_ANCHOR_BOTTOM_RIGHT,
        type: BMAP_NAVIGATION_CONTROL_LARGE
      });
      this.map.addControl(ctrl_nav);
      // let ctrl_ove = new BMap.OverviewMapControl({anchor:BMAP_ANCHOR_BOTTOM_RIGHT,isOpen:1});
      // this.map.addControl(ctrl_ove);
      this.map.addControl(new BMap.ScaleControl()); //比例尺控件，默认位于地图左下方，显示地图的比例关系。
      this.map.addControl(new BMap.MapTypeControl()); //地图类型控件，默认位于地图右上方。
      this.map.addControl(new BMap.CopyrightControl()); //版权控件，默认位于地图左下方。
      //自己地图标点上传信息
      this.map.addEventListener("rightclick", function(e) {
        // console.log(e);
        //
        // console.log( e.point.lng,e.point.lat);
        if (_this.fclickMarker !== null) {
          // alert("a");
          _this.map.removeOverlay(_this.fclickMarker);
          let clickPonit = new BMap.Point(e.point.lng, e.point.lat);
          _this.fclickMarker = new BMap.Marker(clickPonit);
          _this.map.addOverlay(_this.fclickMarker); // 将点击点标注添加到地图中
          // 点击打开上传信息的model
          _this.fclickMarker.addEventListener("click", function(e) {
            // alert("您是想自己上传信息吗？");
            _this.point = e.point;
            _this.formItem.mapPointJ = e.point.lng;
            _this.formItem.mapPointW = e.point.lat;
            _this.uploadModal = true;

            // console.log( _this.point)
          });
        } else {
          console.log(_this.fclickMarker);
          let clickPonit = new BMap.Point(e.point.lng, e.point.lat);
          _this.fclickMarker = new BMap.Marker(clickPonit);
          _this.map.addOverlay(_this.fclickMarker); // 将点击点标注添加到地图中
          // 点击打开上传信息的model
          _this.fclickMarker.addEventListener("click", function(e) {
            // alert("您是想自己上传信息吗？");
            _this.point = e.point;
            _this.formItem.mapPointJ = e.point.lng;
            _this.formItem.mapPointW = e.point.lat;
            _this.uploadModal = true;

            // console.log("点")
            // console.log( _this.point)
          });
          console.log(_this.fclickMarker);
        }
      });

      //初始化地图的相关操作
      this.point = new BMap.Point(jd, wd); // 创建点坐标
      this.map.centerAndZoom(this.point, 15); // 初始化地图，设置中心点坐标和地图级别
      // this.map.enableScrollWheelZoom(true);     //开启鼠标滚轮缩放
      this.buildinglist.forEach(function(item) {
        //创建多标注
        var point2 = new BMap.Point(item.j, item.w);
        var marker = new BMap.Marker(point2); // 创建标注
        _this.map.addOverlay(marker); // 将标注添加到地图中
        marker.addEventListener("click", function(e) {
          _this.point = e.point;
          _this.openInfoView(item);
          console.log(e.point);
        });
      });
    },
    //          removeClick(){
    //              this.map.removeEventListener("click");
    // },

    skiptomap(row, event, column) {
      // console.log(row,column);
      this.point = new BMap.Point(row.j, row.w);
      this.map.centerAndZoom(this.point, 15);
      this.openInfoView(row);
    },
    openInfoView(item) {
      var that = this;
      var dataItem = {
        name: item.name,
        addr: item.addr,
        tel: item.tel,
        mapPointBedNum: item.mapPointBedNum,
        mapPointFee: item.mapPointFee,
        mapPointJian: item.mapPointJian,
        mapPointServer: item.mapPointServer,
        current: item.current,
        showMapPointImage: item.showMapPointImage,
        mapPointId: item.id
      };
      var htmlInfo =
        "<div  style='word-wrap:break-word; '><h3>" +
        dataItem.name +
        "</h3> <hr /><div><p></p>" +
        "<p>详细地址：" +
        dataItem.addr +
        "</p><p>联系电话：" +
        dataItem.tel +
        "</p>" +
        "<p>床位：" +
        dataItem.mapPointBedNum +
        "<span style='font-weight: bold;margin-left: 5px'>张</span></p>" +
        "<p>服务费用：" +
        dataItem.mapPointFee +
        "<span style='font-weight: bold;margin-left: 5px'>起</span></p></p>" +
        "<p >简历：" +
        dataItem.mapPointJian +
        "</p>" +
        "<p>服务：" +
        dataItem.mapPointServer +
        "</p>" +
        "</div></div>";

      var opts = {
        width: 400
      };
      var infoWindow = new BMap.InfoWindow(htmlInfo, opts); // 创建信息窗口对象
      console.log(this.point, infoWindow);
      this.map.openInfoWindow(infoWindow, this.point); //开启信息窗口
      // 增加浏览量
      this.viewFunction(dataItem.mapPointId);
    },
    async getMapPoint() {
      let that = this;
      try {
        const sendPage = that.currentPages;
        const mapPointList = await mapPointGet(sendPage);
        console.log("获取");
        console.log(mapPointList);
        that.buildinglist = [];
        that.dataLength = mapPointList.data.allDateLength;
        for (
          let i = 0, length = mapPointList.data.msg.length;
          i < length;
          i++
        ) {
          that.buildinglist.push({
            current: i,
            id: mapPointList.data.msg[i].mapPointId,
            name: mapPointList.data.msg[i].mapPointName,
            j: mapPointList.data.msg[i].mapPointJ,
            w: mapPointList.data.msg[i].mapPointW,
            addr: mapPointList.data.msg[i].mapPointAddr,
            tel:
              mapPointList.data.msg[i].mapPointTel === null
                ? ""
                : mapPointList.data.msg[i].mapPointTel,
            mapPointBedNum:
              mapPointList.data.msg[i].mapPointBedNum === null
                ? ""
                : mapPointList.data.msg[i].mapPointBedNum,
            mapPointFee:
              mapPointList.data.msg[i].mapPointFee === null
                ? ""
                : mapPointList.data.msg[i].mapPointFee,
            mapPointJian: mapPointList.data.msg[i].mapPointJian,
            mapPointServer: mapPointList.data.msg[i].mapPointServer,
            mapPointImage: mapPointList.data.msg[i].mapPointImage,
            showMapPointImage:
              mapPointList.data.msg[i].mapPointImage.length !== 0
                ? true
                : false,
            mapPointfare: mapPointList.data.msg[i].mapPointfare,
            mapPointViews: mapPointList.data.msg[i].mapPointViews,
            mapPointVedio: mapPointList.data.msg[i].mapPointVedio
          });
        }
        console.log(that.buildinglist);
        that.loadmap(that.buildinglist[0].j, that.buildinglist[0].w);
      } catch (err) {
        console.log(err);
        that.$Message.error("出现错误，请联系管理员");
      }
    },
    async searchFunction() {
      // console.log(this.searchValue);
      let that = this;
      try {
        const sendPage = that.currentPages;
        const searchValue = that.searchValue;
        const mapPointList = await mapPointSearch({ sendPage, searchValue });
        console.log("搜索");
        that.buildinglist = [];
        that.dataLength = mapPointList.data.allDateLength;
        for (
          let i = 0, length = mapPointList.data.msg.length;
          i < length;
          i++
        ) {
          that.buildinglist.push({
            current: i,
            id: mapPointList.data.msg[i].mapPointId,
            name: mapPointList.data.msg[i].mapPointName,
            j: mapPointList.data.msg[i].mapPointJ,
            w: mapPointList.data.msg[i].mapPointW,
            addr: mapPointList.data.msg[i].mapPointAddr,
            tel:
              mapPointList.data.msg[i].mapPointTel === null
                ? ""
                : mapPointList.data.msg[i].mapPointTel,
            mapPointBedNum:
              mapPointList.data.msg[i].mapPointBedNum === null
                ? ""
                : mapPointList.data.msg[i].mapPointBedNum,
            mapPointFee:
              mapPointList.data.msg[i].mapPointFee === null
                ? ""
                : mapPointList.data.msg[i].mapPointFee,
            mapPointJian: mapPointList.data.msg[i].mapPointJian,
            mapPointServer: mapPointList.data.msg[i].mapPointServer,
            mapPointImage: mapPointList.data.msg[i].mapPointImage,
            showMapPointImage:
              mapPointList.data.msg[i].mapPointImage.length !== 0
                ? true
                : false,
            mapPointfare: mapPointList.data.msg[i].mapPointfare,
            mapPointViews: mapPointList.data.msg[i].mapPointViews,
            mapPointVedio: mapPointList.data.msg[i].mapPointVedio
          });
        }
        console.log(that.buildinglist);
        that.loadmap(that.buildinglist[0].j, that.buildinglist[0].w);
      } catch (err) {
        that.$Message.error("未连接网络，请检查网络是否连接");
      }
    },
    clearFunction() {
      this.getMapPoint();
    },
    uploadPoint() {
      this.uploadModal = true;
    },
    async handleSubmit() {
      const _this = this;
      // console.log("haha===========================");
      const {
        mapPointName,
        mapPointJ,
        mapPointW,
        mapPointAddr,
        mapPointTel,
        mapPointBedNum,
        mapPointFee,
        mapPointJian,
        mapPointServer
      } = this.formItem;
      try {
        // console.log("haha");
        const addRes = await addPointInfo({
          mapPointName,
          mapPointJ,
          mapPointW,
          mapPointAddr,
          mapPointTel,
          mapPointBedNum,
          mapPointFee,
          mapPointJian,
          mapPointServer
        });
        if (addRes.data.result === 1) {
          _this.$Message.error(addRes.data.msg);
        } else {
          _this.$Message.success("添加成功");
        }
      } catch (err) {
        _this.$Message.error("未知错误" + err);
      }
      this.getMapPoint();
      this.handleCancel();
    },
    handleCancel() {
      this.uploadModal = false;
      this.formItem = {
        mapPointName: "",
        mapPointJ: "",
        mapPointW: "",
        mapPointAddr: "",
        mapPointTel: "",
        mapPointBedNum: "",
        mapPointFee: "",
        mapPointJian: "",
        mapPointServer: ""
      };
    },
    async viewFunction(currentId) {
      let that = this;
      try {
        const res = await mapPointView(currentId);
        if (res.data.result === 0) {
        }
      } catch (e) {}
    }
  },
  mounted() {
    this.getMapPoint();
  }
};
</script>

<style scoped>
</style>