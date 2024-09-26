<template>
  <el-container style="border: 2px solid #eee;">
    <div ref="echartsContainer" style="width: 7800px; height: 540px;"></div>
  </el-container>
</template>
 
<script>
import * as echarts from 'echarts'
export default {
  name: 'ReportForm',
  data() {
    return {
      years: [],
      year_data: [],
      myChart: null
    }
  },
  created() {
    this.reqInitialData()  // html加载完成前向后台请求数据
  },
  mounted() {
    // console.log('报表统计组件', this)
    // 初始化echarts实例
  },
  methods: {
    async reqInitialData() {
      await this.reqData()
    },
    async reqData() {
      this.$axios
        .get("/userapi/movie_data_report/")
        .then((response) => {
          const data = response.data
          this.years = data.years
          this.year_data = data.year_data

          this.$nextTick(() => {
            this.initChart()
          })
        })
    },
    initChart() {
      if (this.myChart) {
        this.myChart.dispose()
      }
      this.myChart = echarts.init(this.$refs.echartsContainer)

      const option = {
        title: {
          text: '上映时间走势图',
          textStyle: {
            color: '#008000'
          },

          subtext: '电影数/年',
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          }
        },
        toolbox: {
          show: true,
          feature: {
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          data: this.years
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: '{value} 部'
          },
          axisPointer: {
            snap: true
          }
        },
        visualMap: {
          show: false,
          dimension: 0,
          pieces: [
            {
              lte: 73,
              color: 'blue'
            },
            {
              gt: 73,
              lte: 83,
              color: 'red'
            },
            {
              gt: 83,
              lte: 93,
              color: 'blue'
            },
            {
              gt: 93,
              color: 'red'
            },
          ]
        },
        series: [
          {
            name: '部数',
            data: this.year_data,
            type: 'line',
            smooth: true,
            markArea: {
              itemStyle: {
                color: 'rgba(255, 173, 177, 0.4)'
              },
              data: [
                [
                  {
                    name: '2000~2010年',
                    xAxis: '2000'
                  },
                  {
                    xAxis: '2010'
                  }
                ],
                [
                  {
                    name: '2020~2024年',
                    xAxis: '2020'
                  },
                  {
                    xAxis: '2024'
                  }
                ]
              ]
            }
          }
        ]
      }

      console.log('图表配置', option)

      this.myChart.setOption(option)

      //随着屏幕大小调节图表
      window.addEventListener("resize", () => {
        this.myChart.resize();
      })
    }
  }
}
</script>