<template>
  <div style="height: 100%">
    <el-container style="border: 2px solid #eee; height: 100%;">
      <el-header style="border: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; padding: 0 5px;">
        <span style="flex: 1; text-align: left;">国家/地区发片量排行分析</span>
        <span style="flex: 1; text-align: left;">国家/地区发片量构成分析</span>
      </el-header>
      <el-main style="display: flex; padding: 5px; box-sizing: border-box;">
        <div ref="echartsContainer1" style="width: 50%; height: 100%;"></div>
        <div ref="echartsContainer2" style="width: 50%; height: 100%;"></div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import * as echarts from 'echarts'
export default {
  name: 'CountryAnalysis',
  data() {
    return {
      country_type: [],
      country_type_num: [],
      type_num: [],
      myChart1: null,
      myChart2: null
    }
  },
  created() {
    this.reqInitialData()  // html加载完成前向后台请求数据
  },
  mounted() {
    console.log('国家/地区组件', this)
    // 初始化echarts实例
  },
  methods: {
    async reqInitialData() {
      await this.reqData()
    },
    async reqData() {
      this.$axios
        .get("/userapi/country_type/")
        .then((response) => {
          const data = response.data
          this.country_type = data.country_type
          this.country_type_num = data.country_type_num
          this.type_num = data.type_num

          this.$nextTick(() => {
            this.initChart1()
            this.initChart2()
          })
        })
    },
    initChart1() {
      if (this.myChart1) {
        this.myChart1.dispose()
      }
      this.myChart1 = echarts.init(this.$refs.echartsContainer1)

      const option1 = {
        title: {
          text: '各国家/地区电影数',
          textStyle: {
            color: '#3f3fd8'
          },
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        toolbox: {
          show: true,
          feature: {
            saveAsImage: { show: true },  // 导出图片
            dataView: { show: true, readOnly: false }, // 数据视图
            mark: { show: true },
            dataZoom:{ show: true },  // 区域缩放
            magicType: {   // 视图切换
              type: ['line', 'bar']
            },
            restore: { show: true }, // 重置
          }
        },
        grid: {
           width: 'auto',
           hight: 'auto'
        },
        xAxis: [
          {
            type: 'category',
            data: this.country_type,
            axisTick: {
              alignWithLabel: true
            }
          }
        ],
        yAxis: [
          {
            type: 'value',
            axisLabel: {
              formatter: '{value} 部'
            },
          }
        ],
        series: [
          {
            name: '部数',
            type: 'bar',
            data: this.country_type_num,
            itemStyle: {
              borderRadius: [10, 10, 0, 0],
              color: new echarts.graphic.LinearGradient(
                0, 0, 0, 1, // x1, y1, x2, y2 定义渐变方向
                [
                  {offset: 0, color: '#d2b5ec'},
                  {offset: 0.5, color: '#b374ee'},
                  {offset: 1, color: 'blueviolet'}
                ]
              )
            }
          }
        ]
      }

      this.myChart1.setOption(option1)

      //随着屏幕大小调节图表
      window.addEventListener("resize", () => {
        this.myChart1.resize();
      })
    },
    initChart2() {
      if (this.myChart2) {
        this.myChart2.dispose()
      }
      this.myChart2 = echarts.init(this.$refs.echartsContainer2)

      const option2 = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          type: 'scroll',
          orient: 'vertical',
          right: 0,
          top: 30,
          bottom: 20,
        },
        toolbox: {
          show: true,
          feature: {
            saveAsImage: { show: true },  // 导出图片
            dataView: { show: true, readOnly: false }, // 数据视图
            mark: { show: true },
            restore: { show: true }, // 重置
          }
        },
        series: [
          {
            name: '类型构成',
            type: 'pie',
            radius: '58%',
            center: ['42%', '50%'],
            roseType: 'area',
            itemStyle: {
              borderRadius: 8
            },
            data: this.type_num
          }
        ]
      }

      this.myChart2.setOption(option2)

      //随着屏幕大小调节图表
      window.addEventListener("resize", () => {
        this.myChart2.resize();
      })
    }
  }
}
</script>

<style scoped>
.el-header {
  height: 20px;
  color: rgb(17, 44, 180);
  font-size: 16px;
}
</style>