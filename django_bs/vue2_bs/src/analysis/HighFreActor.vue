<template>
  <div style="height: 100%;">
    <el-container style="border: 2px solid #eee; height: 100%;">
      <el-header style="border: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; padding: 0 5px;">
        <span>高频演员词云图</span>
      </el-header>
      <el-main style="display: flex; padding: 5px; box-sizing: border-box;">
        <div class="wordcloud-container" ref="wordcloudRef"></div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import 'echarts-wordcloud'
export default {
  name: 'HighFreActor',
  data() {
    return {
      actor_num: [],
      myChart: null,
    }
  },
  created() {
    this.reqInitialData()  // html加载完成前向后台请求数据
  },
  mounted() {
    console.log('高频演员组件', this)
  },
  methods: {
    async reqInitialData() {
      await this.reqData()
    },
    async reqData() {
      this.$axios
        .get("/userapi/high_freActor/")
        .then((response) => {
          const data = response.data
          this.actor_num = data.actor_num

          this.$nextTick(() => {
            this.initChart()
          })
        })
    },
    initChart() {
      if (this.myChart) {
        this.myChart.dispose()
      }
      // 初始化 ECharts 实例
      this.myChart = echarts.init(this.$refs.wordcloudRef)
 
      // 指定图表的配置项和数据
      const option = {
        tooltip: {},
        series: [{
          type: 'wordCloud',
          sizeRange: [10, 60],
          rotationRange: [-90, 90],
          rotationStep: 45,
          gridSize: 8,
          shrinkToFit: true,
          shape: 'pentagon', // 可以是 'circle', 'cardioid', 'diamond', 'triangle-forward', 'triangle', 'pentagon', 'star'
          width: '70%',
          height: '90%',
          left: 'center',
          top: 'center',
          textStyle: {
              color: function () {
                  return 'rgb(' + [
                      Math.round(Math.random() * 160),
                      Math.round(Math.random() * 160),
                      Math.round(Math.random() * 160)
                  ].join(',') + ')';
              }
          },
          data: this.actor_num
        }]
      };
      
      console.log('词云图表配置', option)

      // 使用刚指定的配置项和数据显示图表。
      this.myChart.setOption(option)

      //随着屏幕大小调节图表
      window.addEventListener("resize", () => {
        this.myChart.resize();
      })
    }
  }
}
</script>

<style scoped>
.el-header {
  height: 30px;
  color: orange;
  font-size: 16px;
}
.wordcloud-container {
  width: 100%;
  height: 100%;
}
</style>