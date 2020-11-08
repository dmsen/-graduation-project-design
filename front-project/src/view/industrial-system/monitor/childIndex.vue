<template>
  <div>
    <Card :dis-hover="true" class="headerCard">
      <Select
        v-model="equipmentId"
        filterable
        placeholder="请选择机器"
        label-in-value
        @on-change="handleChooseMac"
      >
        <Option v-for="item in equipmentList" :value="item.id" :key="item.id">{{
          item.name
        }}</Option>
      </Select>
    </Card>
    <Card :dis-hover="true">
      <Rate :value="1" :count="1" character="采用了 websocket 实时推送数据" />
      <Rate
        :value="1"
        :count="1"
        character=",在监测点配置页面配置机器监测点即可查看"
      />
    </Card>
    <Card
      :dis-hover="true"
      v-show="equipmentId"
      style="margin: 0 0px 20px 0px; "
    >
      <Row style="margin: -20px 0 0 -20px">
        <i-col
          :xs="12"
          :md="8"
          :lg="4"
          v-for="(infor, i) in inforCardData"
          :key="`infor-${i}`"
          style="height: 120px;padding: 10px;"
        >
          <infor-card
            shadow
            :color="themeColor"
            :icon="infor.icon"
            :icon-size="36"
            style="margin: 12px"
          >
            <count-to :end="infor.count" count-class="count-style" />
            <p>{{ infor.title }}</p>
          </infor-card>
        </i-col>
      </Row>
    </Card>
    <Card :dis-hover="true">
      <div id="lineChart"></div>
    </Card>
  </div>
</template>
<script>
const themeColor =
  localStorage.themeStyle === "dark"
    ? "#666"
    : localStorage.themeStyle === "blue"
    ? "#4884e2"
    : localStorage.themeStyle === "light"
    ? "#19be6b"
    : "#ffa3d5";
import HighCharts from "highcharts/highstock";
import boost from "highcharts/modules/boost.js";
import theme from "highcharts/themes/grid-light.js";
theme(HighCharts);
boost(HighCharts);
HighCharts.setOptions({
  global: {
    timezoneOffset: 8 * 60,
    useUTC: false
  },
  colors: [themeColor]
});
// var a = document.getElementById('domId')
// new Highcharts.Chart(a,{
//   series: []
// })
// var chart = new HighCharts.Chart('domId',{
//   series: []
// })

// var options = {
//   chart: {
//     renderTo: 'domId' // 或 renderTo: document.getElementById('contianer')
//   },
// }
// var chart = new Highcharts.chart(options);
import { getAlarmMsg } from "@/api/alarm.js";
// import { wsConnect } from "@/api/index.js";
import { getMachines } from "@/api/equipment.js";
import { errMessage } from "@/api/index.js";
import CountTo from "_c/count-to";
import InforCard from "_c/info-card";
import config from "@/config";
const websocketUrl = config.baseUrl.websocketUrl;
let list = new Map();
let times = 0;
let times2 = 0;
export default {
  components: {
    CountTo,
    InforCard
  },
  data() {
    return {
      websock: null,
      themeColor: themeColor,
      charts: null,
      dataArray: [],
      inforCardData: [],
      equipmentList: [],
      equipmentId: "",
      numC: true,
      list: null,
      alarmInterval: null
    };
  },
  methods: {
    async getMachines() {
      try {
        this.equipmentList = [];
        const machineList = await getMachines();
        for (let i = 0, length = machineList.data.msg.length; i < length; i++) {
          this.equipmentList.push({
            id: machineList.data.msg[i].machineId,
            name: machineList.data.msg[i].machineName
          });
        }
      } catch (err) {
        if (err.response !== undefined) {
          errMessage(err.response.status);
        } else {
          errMessage(1);
        }
      }
    },
    handleChooseMac() {
      let that = this;
      // let macId = that.$store.state.monitor.machId
      this.dataArray = [];
      this.numC = true;
      this.clearLine();
      this.$store.commit("setMachId", this.equipmentId);
      if (this.charts !== null) {
        for (let i = 0; i < that.charts.series.length; i++) {
          that.charts.series[i].remove();
        }
      }
      if (that.websock.readyState === 3) {
        this.initWebpack();
        that.webSocket(this.equipmentId);
      } else {
        that.websock.send(this.equipmentId);
      }
    },
    clearLine() {
      this.charts && this.charts.destroy();
      this.charts = null;
      list = null;
      list = new Map();
      this.inforCardData = [];
    },

    initWebpack() {
      //初始化websocket
      // this.websock = new WebSocket('ws://112.74.59.53/websocket'); //这里面的this都指向vue
      this.websock = new WebSocket(websocketUrl);
      // if(this.$store.state.monitor.isGeneralChoose){
      //    this.webSocket(this.$store.state.monitor.machId)
      // }else{
      //       this.webSocket(-1)
      // }
    },
    webSocket(id) {
      let that = this;
      this.websock.onopen = () => {
        // Web Socket 已连接上，使用 send() 方法发送数据
        that.websock.send(id);
      };
      this.websock.onmessage = res => {
        // console.log(res)
        // res = JSON.stringify(res)
        // console.log(res)
        res = JSON.parse(res.data);
        console.log(res);
        const temp = new Date().getTime();
        if (res.machineId === this.equipmentId) {
          if (list.get(res.physicalName) !== undefined) {
            if (list.get(res.physicalName).length > 40) {
              list.get(res.physicalName).shift();
            } else {
              list.get(res.physicalName).push([res.time, res.value]);
            }
          } else {
            list.set(res.physicalName, [[res.time, res.value]]);
          }
          if (that.numC === true) {
            if (
              that.dataArray.length === 0 ||
              that.dataArray[0].name !== res.physicalName
            ) {
              that.dataArray.push({
                name: res.physicalName,
                data: [[res.time, res.value]]
              });
            } else {
              that.numC = false;
              that.charts = new HighCharts.Chart("lineChart", {
                plotOptions: {
                  series: {
                    cursor: "pointer",
                    allowPointSelect: true,
                    animation: true
                  }
                },
                credits: {
                  enabled: false
                },
                xAxis: {
                  type: "datetime",
                  dateTimeLabelFormats: {
                    millisecond: "%H:%M:%S.%L",
                    second: "%H:%M:%S",
                    minute: "%H:%M",
                    hour: "%H:%M",
                    day: "%m-%d",
                    week: "%m-%d",
                    month: "%Y-%m",
                    year: "%Y"
                  }
                },
                title: { text: "实时参数监控" },
                series: that.dataArray
              });
            }
          }
          // console.log(that.dataArray)
          setTimeout(function() {
            for (let z = 0; z < that.dataArray.length; z++) {
              if (res.physicalName === that.dataArray[z].name) {
                try {
                  if (that.dataArray[z].data.length < 15) {
                    that.charts.series[z].addPoint([res.time, res.value]);
                  } else {
                    that.charts.series[z].addPoint(
                      [res.time, res.value],
                      true,
                      true
                    );
                  }
                } catch (e) {
                  // console.log(e)
                }
              }
            }
          }, 2000);
          let _i = 0;
          if (temp - times > 2000) {
            times = temp;
            for (let [key, value] of list.entries()) {
              this.inforCardData.splice(_i, 1, {
                title: key,
                count: value[value.length - 1][1]
              });
              _i++;
            }
          }
          _i = 0;
        } else if (typeof res !== Object) {
          if (res > 0) {
            this.$Message.error({
              duration: 1.5,
              content:
                "当前有异常数据！！！共" + res + "条" + " ,请查看异常记录"
            });
          }
          // this.$Message.warning("该机器无数据！");
        }
      };
      this.websock.onerror = function(e) {
        that.$Message.success({
          content: "连接断开",
          duration: 1
        });
        // setTimeout(function(){
        //     window.location.reload();
        // },600)
      };
      this.websock.onclose = function() {
        // 关闭 websocket
        // console.log('连接已关闭...')
      };
      // 路由跳转时结束websocket链接
      this.$router.afterEach(function() {
        // that.websock.send("999");
        that.websock.close();
      });
    },

    initWebSocket() {
      let msg = "1:" + this.equipmentId;
      this.socketApi.initWebSocket();
      this.socketApi.sendSock(msg, this.getSocketVal);
    },
    getSocketVal(res) {
      let that = this;
      res = JSON.stringify(res);
      res = JSON.parse(res);
      console.log(res);
      const temp = new Date().getTime();
      if (res.machineId === this.equipmentId) {
        if (list.get(res.physicalName) !== undefined) {
          if (list.get(res.physicalName).length > 40) {
            list.get(res.physicalName).shift();
          } else {
            list.get(res.physicalName).push([res.time, res.value]);
          }
        } else {
          list.set(res.physicalName, [[res.time, res.value]]);
        }
        if (that.numC === true) {
          if (
            that.dataArray.length === 0 ||
            that.dataArray[0].name !== res.physicalName
          ) {
            that.dataArray.push({
              name: res.physicalName,
              data: [[res.time, res.value]]
            });
          } else {
            that.numC = false;
            that.charts = new HighCharts.Chart("lineChart", {
              plotOptions: {
                series: {
                  cursor: "pointer",
                  allowPointSelect: true,
                  animation: true
                }
              },
              credits: {
                enabled: false
              },
              xAxis: {
                type: "datetime",
                dateTimeLabelFormats: {
                  millisecond: "%H:%M:%S.%L",
                  second: "%H:%M:%S",
                  minute: "%H:%M",
                  hour: "%H:%M",
                  day: "%m-%d",
                  week: "%m-%d",
                  month: "%Y-%m",
                  year: "%Y"
                }
              },
              title: { text: "实时参数监控" },
              series: that.dataArray
            });
          }
        }
        // console.log(that.dataArray)
        // setTimeout(function () {
        for (let z = 0; z < that.dataArray.length; z++) {
          if (res.physicalName === that.dataArray[z].name) {
            try {
              if (that.dataArray[z].data.length < 15) {
                that.charts.series[z].addPoint([res.time, res.value]);
              } else {
                that.charts.series[z].addPoint(
                  [res.time, res.value],
                  true,
                  true
                );
              }
            } catch (e) {
              // console.log(e)
            }
          }
        }
        // },2000);
        let _i = 0;
        if (temp - times > 2000) {
          times = temp;
          for (let [key, value] of list.entries()) {
            this.inforCardData.splice(_i, 1, {
              title: key,
              count: value[value.length - 1][1]
            });
            _i++;
          }
        }
        _i = 0;
      } else if (typeof res !== Object) {
        // if (res > 0) {
        //   this.$Message.error({
        //     duration: 1.5,
        //     content: "当前有异常数据！！！共" + res + "条" +" ,请查看异常记录"
        //   });
        // }
        // this.$Message.warning("该机器无数据！");
      }
    },
    async getMsgCall(res) {
      try {
        // const res= await getAlarmMsg();
        // // console.log(res)
        // this.$Message.error({
        //   duration: 1.5,
        //   content: "当前有异常数据！！！共" + res.data.msg + "条"+" ,请查看异常记录"
        // });
      } catch (err) {}
    }
  },
  // created:function () {
  // console.log('嘎嘎嘎')
  // },
  mounted: function() {
    this.getMachines();
    // let that = this
    //
    // this.initWebpack();
    // console.log("设备id"+that.$store.state.monitor.machId)
    // console.log (this.$store.state.monitor.isGeneralChoose)
    // if (this.$store.state.monitor.isGeneralChoose) {
    //     that.dataArray = [];
    //     that.numC = true;
    //     that.clearLine();
    //     if(that.charts !== null){
    //         for(let i = 0;i < that.charts.series.length ; i++){
    //             that.charts.series[i].remove()
    //         }
    //       }
    //     that.equipmentId = that.$store.state.monitor.machId;
    //     that.webSocket(that.$store.state.monitor.machId.toString())
    //     // that.webSocket(that.$store.state.monitor.machId)
    //     console.log('----------------------------')
    // }else{
    //   this.$Message.error('未选择设备，请前往父页选择设备')
    //   this.$router.push('/industrialSystem/dynamicDate1')
    // }
  },

  beforeRouteLeave(to, from, next) {
    // 导航离开该组件的对应路由时调用
    // 可以访问组件实例 `this`
    next();
    // const answer = window.confirm('Do you really want to leave? you have unsaved changes!')
    // if (answer) {
    //   next()
    // } else {
    //   next(false)
    // }
  },
  beforeRouteEnter(to, from, next) {
    //  next((vm) => {})
    try {
      next(vm => {
        let that = vm;
        that.dataArray = [];
        that.numC = true;
        that.clearLine();
        if (that.charts !== null) {
          for (let i = 0; i < that.charts.series.length; i++) {
            that.charts.series[i].remove();
          }
        }
        if (that.$store.state.monitor.machId) {
          if (that.websock === null) {
            that.initWebpack();
            console.log(
              that.$store.state.monitor.machId,
              typeof that.$store.state.monitor.machId
            );
            that.equipmentId = that.$store.state.monitor.machId;
            console.log(that.$store.state.monitor.isGeneralChoose);
            that.webSocket(that.$store.state.monitor.machId);
          } else {
            console.log("that.websock");
            console.log(that.websock);
            console.log(
              that.$store.state.monitor.machId,
              typeof that.$store.state.monitor.machId
            );
            // 设置延时 防止跳转过快导致页面bug，websocket还在关闭中
            setTimeout(function() {
              that.initWebpack();
              that.equipmentId = that.$store.state.monitor.machId;
              that.webSocket(that.$store.state.monitor.machId);
            }, 1000);
          }
        } else {
          that.$Message.error("未选择设备，请前往父页选择设备");
          that.$router.push("/industrialSystem/dynamicDate1");
        }

        //   if (that.$store.state.monitor.isGeneralChoose) {
        //   that.getMachines();
        //  that.initWebpack();
        //   that.dataArray = [];
        //   that.numC = true;
        //   that.clearLine();
        //   if(that.charts !== null){
        //         for(let i = 0;i < that.charts.series.length ; i++){
        //             that.charts.series[i].remove()
        //         }
        //       }
        //   console.log("测试")
        //   console.log(that.websock)
        // if(that.websock.readyState===3){
        //    that.equipmentId = that.$store.state.monitor.machId;
        //    that.initWebpack()
        //    that.webSocket(that.$store.state.monitor.machId.toString())
        //   //  that.websock.send(that.$store.state.monitor.machId.toString())
        // // that.initWebpack()
        // //   that.webSocket(that.$store.state.monitor.machId.toString())
        // }
        // else{
        //   console.log("不肯")
        //   // that.webSocket(that.$store.state.monitor.machId.toString())
        //   //  that.websock.send(that.$store.state.monitor.machId.toString())
        // }
        //   }else{
        //          that.$Message.error('未选择设备，请前往父页选择设备')
        //          that.$router.push('/industrialSystem/dynamicDate1')
        //   }

        //vm就是当前组件实例
      });
    } catch (err) {
      console.log("错误");
      console.log(err);
    }
  }
};
</script>
<style lang="less">
.count-style {
  font-size: 40px;
}
</style>

