<template>
  <div style="height: 525px; background-color: #e0e0e0;">
    <el-row>
      <el-col :span="24" style="display: flex; flex-direction: column;">
        <el-row style="flex: 1; background-color: #fff; margin-bottom: 5px; height: 100%; padding: 2px;">
          <ShortCommentDataTongji />
        </el-row>

        <el-row style="flex: 1; background-color: #fff; margin-bottom: 5px; height: 100%; padding: 2px;">
          <ReportForm />
        </el-row>

        <el-row style="flex: 1; background-color: #fff; height: 100%; padding: 2px;">
          <WordCloud />
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import ShortCommentDataTongji from './ShortCommentDataTongji.vue'
import ReportForm from './ReportForm.vue'
import WordCloud from './WordCloud.vue'
export default {
  name: 'ShortCommentDashBoard',
  components: { ShortCommentDataTongji, ReportForm, WordCloud },
  mounted() {
    console.log("短评数据统计组件加载完成", this)
  },
  beforeDestroy() {
    console.log("短评数据统计组件即将销毁")
  },
}
</script>

<style>
.background-color {
  background-color: #fff;
}
</style>