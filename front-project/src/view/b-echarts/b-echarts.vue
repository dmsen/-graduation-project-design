<template>
  <div>
    <h1>bEcharts</h1>
    <div
      id="main"
      style="width: 680px; height: 400px; -moz-user-select: none;"
      _echarts_instance_="ec_1532416199070"
    >
      <div
        style="position: relative; overflow: hidden; width: 300px; height: 200px; padding: 0px; margin: 0px; border-width: 0px; cursor: default;"
      ></div>
    </div>
  </div>
</template>

<script>
import { getjson } from "@/api/dataJson.js";
export default {
  data() {
    return {
      myChartdata: null,
      myChart: null
    };
  },
  methods: {
    async getJson() {
      let myChart = this.$echarts.init(document.getElementById("main"));
      // getjson().then(res => {
      //   console.log("111111");
      //   let data = res.data.msg;
      //   console.log(data, typeof data);
      // });
      let res = await getjson();
      this.myChartdata = res.data.msg;
      // console.log("数据");
      console.log(this.myChartdata, typeof this.myChartdata);
      // this.data = console.log(res.data, typeof res.data);
    },
    draw() {
      console.log("hahaha");
      console.log(this.myChart);
      console.log(this.myChartdata);
      const data = this.myChartdata;
      // option = {};
      this.myChart.setOption(
        {
          title: {
            text: "ChangSha AQI"
          },
          tooltip: {
            trigger: "axis"
          },
          xAxis: {
            data: data.map(function(item) {
              return item[0];
            })
          },
          yAxis: {
            splitLine: {
              show: false
            }
          },
          toolbox: {
            left: "center",
            feature: {
              dataZoom: {
                yAxisIndex: "none"
              },
              restore: {},
              saveAsImage: {}
            }
          },
          dataZoom: [
            {
              startValue: "2018-01-01"
            },
            {
              type: "inside"
            }
          ],
          visualMap: {
            top: 10,
            right: 10,
            pieces: [
              {
                gt: 0,
                lte: 50,
                color: "#096"
              },
              {
                gt: 50,
                lte: 100,
                color: "#ffde33"
              },
              {
                gt: 100,
                lte: 150,
                color: "#ff9933"
              },
              {
                gt: 150,
                lte: 200,
                color: "#cc0033"
              },
              {
                gt: 200,
                lte: 300,
                color: "#660099"
              },
              {
                gt: 300,
                color: "#7e0023"
              }
            ],
            outOfRange: {
              color: "#999"
            }
          },
          series: {
            name: "ChangSha AQI",
            type: "line",
            data: data.map(function(item) {
              return item[1];
            }),
            markLine: {
              silent: true,
              data: [
                {
                  yAxis: 50
                },
                {
                  yAxis: 100
                },
                {
                  yAxis: 150
                },
                {
                  yAxis: 200
                },
                {
                  yAxis: 300
                }
              ]
            }
          }
        }
      );
    }
  },

  mounted() {
    // let myChart = this.$echarts.init(document.getElementById("main"));
    // console.log(myChart);
    this.getJson();
    let that = this;
    this.myChart = that.$echarts.init(document.getElementById("main"));
    setTimeout(function() {
      that.draw();
    }, 1000);
  }
};
</script>

<style>
</style>