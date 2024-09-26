<template>
  <div style="height: 100%;">
    <el-container style="border: 2px solid #eee; height: 100%;">
      <el-header style="border: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; padding: 0 5px;">
        <span style="flex: 1; text-align: left;">电影类型发片量排行分析</span>
        <span style="flex: 1; text-align: left;">电影类型发片量构成分析</span>
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
  name: 'TypeAnalysis',
  data() {
    return {
      movie_type: [],
      movie_type_num: [],
      type_num: [],
      myChart1: null,
      myChart2: null
    }
  },
  created() {
    this.reqInitialData()  // html加载完成前向后台请求数据
  },
  mounted() {
    console.log('电影类型组件', this)
    // 初始化echarts实例
  },
  methods: {
    async reqInitialData() {
      await this.reqData()
    },
    async reqData() {
      this.$axios
        .get("/userapi/movie_type/")
        .then((response) => {
          const data = response.data
          this.movie_type = data.movie_type
          this.movie_type_num = data.movie_type_num
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
          text: '各类型电影数',
          textStyle: {
            color: '#8a2be2'
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
            data: this.movie_type,
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
            data: this.movie_type_num,
            itemStyle: {
              borderRadius: [10, 10, 0, 0],  // 圆角
              color: new echarts.graphic.LinearGradient(
                0, 0, 0, 1, // x1, y1, x2, y2 定义渐变方向
                [
                  {offset: 0, color: '#9696ee'},
                  {offset: 0.5, color: '#5c5cec'},
                  {offset: 1, color: 'blue'}
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
            radius: '60%',
            center: ['40%', '50%'],
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
  color: rgb(76, 7, 140);
  font-size: 16px;
}
</style>