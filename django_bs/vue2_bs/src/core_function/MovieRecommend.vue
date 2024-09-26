<template>
  <div style="height: 100%;">
    <el-container>
      <el-header style="height: 25px;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
          <el-row>
            <el-input style="width: 220px; margin-right: 10px" placeholder="请输入电影名称" prefix-icon="el-icon-search"
              v-model="searchMovieName">
            </el-input>
            <el-button type="primary" icon="el-icon-search" round @click="initialSearch">搜索</el-button>
            <el-button type="success" icon="el-icon-refresh-left" round @click="reset">重置</el-button>
          </el-row>
          <!-- 说明弹框部分 -->
          <el-button type="text" @click="open">推荐说明</el-button>
        </div>
      </el-header>
      <el-main>
        <div class="movie-list" v-if="movies.length > 0">
          <div class="movie-item" v-for="(movie, index) in movies" :key="index">
            <div class="movie-left">
              <h4>{{ movie.movieName }}</h4>
              <!-- 电影海报 -->
              <el-image :src="movie.imageUrl" fit="cover" style="width: 170px; height: 200px;"></el-image>
              <el-rate :value="movie.movieScoring/2" disabled show-score text-color="#ff9900"
                :score-template="`${movie.movieScoring}`">
              </el-rate>
              <p>评论人数：{{ movie.commentNumber }}</p>
              <p>{{ movie.movieType }}</p>
              <p>上映日期: {{ movie.releaseInfo }}</p>
              <p>片长: {{ movie.duration }}</p>
              <p>语言: {{ movie.languages }}</p>
              <p>制片国家/地区: {{ movie.movieCountry }}</p>
            </div>

            <div class="movie-right">
              <p>导演：{{ movie.director }}</p>
              <p>
                主演：
                <span>
                  {{ movie.actors.length > truncateLimit ? (showMoreActors[index] ? movie.actors :
                  truncatedActors(movie.actors)) : movie.actors }}
                </span>
                <el-button v-if="movie.actors.length > truncateLimit" @click="toggleMore(index, 'actors')" type="text">
                  {{ showMoreActors[index] ? '收起' : '更多' }}
                </el-button>
              </p>
              <p>
                简介：
                <span>
                  {{ movie.introduction.length > truncateLimit ? (showMoreIntroduction[index] ? movie.introduction :
                  truncatedIntroduction(movie.introduction)) : movie.introduction }}
                </span>
                <el-button v-if="movie.introduction.length > truncateLimit" @click="toggleMore(index, 'introduction')"
                  type="text">
                  {{ showMoreIntroduction[index] ? '收起' : '更多' }}
                </el-button>
              </p>
            </div>
          </div>
        </div>
        <div v-else style="text-align: center; padding: 20px;">
          加载中......
        </div>
        <div
          style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 5px; font-size: 10px;">
          <ul class="pagination" v-html="pageString"></ul>
        </div>
      </el-main>
      <el-backtop target=".page-component__scroll .el-scrollbar__wrap"></el-backtop>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'MovieRecommend',
  data() {
    return {
      searchMovieName: '', // 搜索关键字
      movies: [], // 电影数据
      pageString: '',
      totalPages: 0,  // 总页码
      currentPage: 1,  // 默认页码
      searchPage: 1,   // 搜索框的页码

      showMoreActors: [],
      showMoreIntroduction: [],
      truncateLimit: 165  // 根据需要设置合适的字符限制
    }
  },
  created() {
    this.initialData();
    console.log('电影库组件将被创建', this)
  },
  methods: {
    open() {
      this.$alert('本系统电影推荐功能基于推荐算法：深度神经网络+神经协调过滤。输入电影名称，我们将为你推荐与之相似的、评分前8的电影。', 
        '电影推荐说明', {
        confirmButtonText: '确定',
        callback: action => {
          this.$message({
            type: 'info',
            message: `action: ${ action }`
          })
        }
      })
    },
    // 初始化数据
    async initialData() {
      await this.reqData(this.currentPage)
    },
    async reqData(page) {
      this.$axios
        .post("/userapi/movie_library/", {
          page: page
        })
        .then((response) => {
          const data = response.data
          this.handleReturnData(data, page, 1)
          window.scrollTo(0, 0) // 确保滚动到顶部
        })
    },

    // 搜索方法，可调用后端接口获取数据
    initialSearch() {
      this.search(1)
    },
    search(page) {
      if(this.searchMovieName) {
        this.$axios
          .post("/userapi/movie_recommend/", {
            searchMovieName: this.searchMovieName,
            page: page
          })
          .then((response) => {
            if(response.data.code === 200) {
              //利用ElementUI信息提示组件返回登录信息
              this.$message({
                message: response.data.msg,
                type: 'success'
              })
              const data = response.data
              this.handleReturnData(data, page, 2)
              window.scrollTo(0, 0) // 确保滚动到顶部
            }
            else if(response.data.code === 404) {
              //弹出登录失败信息
							this.$message.error(response.data.msg)
            }
            else {
              alert('查询失败!')
            }
          })
      } else {
        alert('搜索不能为空！')
      }
    },

    reset() {  // 页面重置
      this.reqData(1)
    },
    jump(who) {  // 页码跳转
      // 获取 input 元素
      const pageInput = document.querySelector('#pageInput');
      // 将 input 的值赋给 searchPage
      this.searchPage = pageInput.value;
      const pageNumber = parseInt(this.searchPage, 10);
      if (!isNaN(pageNumber) && pageNumber > 0 && pageNumber <= this.totalPages) {
        if (who === 1) {
          this.reqData(pageNumber)
        } else {
          this.search(pageNumber)
        }
      } else {
        alert('请输入有效的页码')
      }
    },

    handleReturnData(data, page, who) {
      // 更新页面内容
      this.movies = data.movies
      this.pageString = data.page_string
      this.totalPages = data.total_pages
      this.currentPage = page

      // 使用 $nextTick 确保 DOM 已更新
      this.$nextTick(() => {
        // 绑定事件到分页链接
        document.querySelectorAll('.pagination a').forEach(link => {
          link.addEventListener('click', event => {
            event.preventDefault()
            const page = parseInt(event.target.getAttribute('data-page'), 10)
            if (who === 1) {
              this.reqData(page)
            } else {
              this.search(page)
            }
          })
        })

        // 绑定搜索按钮事件
        const searchButton = document.querySelector('#searchButton');
        if (searchButton) {
          searchButton.addEventListener('click', () => {
            this.jump(who) // 这里传入参数 who
          })
        }
      })
    },

    toggleMore(index, type) {
      if (type === 'actors') {
        this.$set(this.showMoreActors, index, !this.showMoreActors[index])
      } else if (type === 'introduction') {
        this.$set(this.showMoreIntroduction, index, !this.showMoreIntroduction[index])
      }
    },
    truncatedActors(actors) {
      return actors.length > this.truncateLimit ? actors.substring(0, this.truncateLimit) + '...' : actors
    },
    truncatedIntroduction(introduction) {
      return introduction.length > this.truncateLimit ? introduction.substring(0, this.truncateLimit) + '...' : introduction
    },
    shouldShowMoreActors(actors) {
      return actors.length > this.truncateLimit
    },
    shouldShowMoreIntroduction(introduction) {
      return introduction.length > this.truncateLimit
    }
  }
}
</script>

<style scoped>
.movie-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between; /* 电影项之间水平间距均匀分布 */
  max-width: 100%; /* 限制最大宽度 */
}
.movie-item {
  width: calc(50% - 10px); /* 四分之一宽度减去间距 */
  margin-bottom: 10px; /* 电影项之间的垂直间距 */
  display: flex;
  border: 2px solid #eee;
}
.movie-left {
  flex: 1;
  padding: 2px;
  text-align: center;
}
.movie-right {
  flex: 1;
}
</style>