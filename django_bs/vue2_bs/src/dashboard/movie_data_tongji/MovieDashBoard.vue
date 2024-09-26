<template>
  <div>
    <el-row>
      <el-col :span="16" style="display: flex; flex-direction: column;">
        <el-row style="flex: 1; background-color: #e0e0e0; margin-bottom: 5px;">
          <el-col :span="24">
            <!-- 左侧上部区域内容 -->
            <div style="height: 116px; padding: 2px;">
              <DataTongji />
            </div>
          </el-col>
        </el-row>

        <el-row style="flex: 1; background-color: #e0e0e0;">
          <el-col :span="24">
            <!-- 左侧下部区域内容 -->
            <div style="height: 550px; padding: 2px;">
              <ReportForm />
            </div>
          </el-col>
        </el-row>
      </el-col>

      <el-col :span="8" style="display: flex; flex-direction: column;">
        <!-- 右侧区域内容 -->
        <el-row style="flex: 1; background-color: #e0e0e0;">
          <el-col :span="24">
            <div style="height: 671px; padding: 5px;">
              <HighScoreFilm />
            </div>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import DataTongji from './DataTongji.vue'
import ReportForm from './ReportForm.vue'
import HighScoreFilm from './HighScoreFilm.vue'
export default {
  name: 'MovieDashBoard',
  components: { DataTongji, ReportForm, HighScoreFilm },
  mounted() {
    console.log("电影数据统计组件", this)
  },
  beforeDestroy() {
    console.log("电影数据统计组件即将被销毁")
  },
}
</script>

<style>

</style>