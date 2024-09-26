<template>
  <el-container style="border: 2px solid #eee;">
    <el-header style="height: 20px;">
      <span style="color: #008000; font-size: 16px;">电影数据统计</span>
    </el-header>
    <el-main>
      <div style="margin-bottom: 5px;">
        <el-row :gutter="20">
          <el-col :span="8">
            <div>
              <el-statistic title="总电影数" :value="movieNumber" group-separator=",">
              </el-statistic>
            </div>
          </el-col>
          <el-col :span="8">
            <div>
              <el-statistic title="平均评分" :value="averageRating" :precision="2" decimal-separator=".">
              </el-statistic>
            </div>
          </el-col>
          <el-col :span="8">
            <div>
              <el-statistic title="总评论人数" :value="total_commentPeopleNumber" group-separator=",">
              </el-statistic>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-main>
  </el-container>
</template>

<script>
export default {
  name: 'DataTongji',
  data() {
    return {
      movieNumber: 0,
      averageRating: 0,
      total_commentPeopleNumber: 0
    }
  },
  created() {
    this.reqInitialData()  // html加载完成前向后台请求数据
    console.log('统计电影数据组件将被创建', this)
  },
  methods: {
    async reqInitialData() {
      await this.reqData()
    },
    async reqData() {
      this.$axios
        .get("/userapi/movie_data_tongji/")
        .then((response) => {
          const data = response.data
          this.movieNumber = data.total_movies,
          this.averageRating = data.average_rating,
          this.total_commentPeopleNumber = data.total_commentPeopleNumber
        })
    }
  },
}
</script>

<style>

</style>