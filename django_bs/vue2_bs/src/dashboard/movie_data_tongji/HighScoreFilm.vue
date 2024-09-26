<template>
  <div>
    <el-table :data="movies" style="width: 100%" max-height="650px">
      <el-table-column prop="movieName" label="高分电影" width="150" show-overflow-tooltip class-name=".el-tooltip__popper">
      </el-table-column>
      <el-table-column prop="movieType" label="" width="150" show-overflow-tooltip class-name=".el-tooltip__popper">
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'HighScoreFilm',
  data() {
    return {
      movies: [],
    }
  },
  created() {
    this.reqInitialData(); // 组件挂载后获取数据
    // console.log('高分电影组件被创建', this)
  },
  methods: {
    // 初始化数据
    async reqInitialData() {
      await this.reqData(this.currentPage)
    },
    async reqData() {
      this.$axios
        .get("/userapi/high_score_films/")
        .then((response) => {
          const data = response.data
          this.movies = data.movies
        })
    },
  }
}
</script>

<style scoped>

</style>