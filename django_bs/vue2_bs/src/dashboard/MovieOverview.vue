<template>
  <div>
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 5px;">
      <el-row>
        <el-input
          style="width: 220px;margin-right: 10px"
          placeholder="请输入关键字"
          prefix-icon="el-icon-search"
          v-model="searchKeys">
        </el-input>
        <el-button type="primary" icon="el-icon-search" round @click="initialSearch">搜索</el-button>
        <el-button type="success" icon="el-icon-refresh-left" round @click="reset">重置</el-button>
      </el-row>
      <!-- <input style="width: 61.33px; height: 37.33px;" type="text" placeholder="页码">
      <button style="width: 61.33px; height: 37.33px; margin-left: 5px" class="btn-primary" @click="search">搜索</button>
      <button style="width: 61.33px; height: 37.33px; margin-left: 5px" class="btn-primary" @click="search">重置</button> -->
    </div>
    <el-table style="width: 100%; height: 100%;" border :data="movies">
      <el-table-column fixed="left" prop="movieID" label="电影ID" show-overflow-tooltip class-name=".el-tooltip__popper">
      </el-table-column>
      <el-table-column prop="movieName" label="电影名称" show-overflow-tooltip class-name=".el-tooltip__popper">
      </el-table-column>
      <el-table-column prop="releaseInfo" label="上映时间" show-overflow-tooltip class-name=".el-tooltip__popper">
      </el-table-column>
      <el-table-column prop="movieScoring" label="评分" show-overflow-tooltip class-name=".el-tooltip__popper">
      </el-table-column>
      <el-table-column prop="commentNumber" label="评论人数" show-overflow-tooltip class-name=".el-tooltip__popper">
      </el-table-column>
      <el-table-column prop="mainActor" label="主要演员" show-overflow-tooltip class-name=".el-tooltip__popper">
      </el-table-column>
      <el-table-column prop="movieType" label="类型" show-overflow-tooltip class-name=".el-tooltip__popper">
      </el-table-column>
      <el-table-column prop="movieCountry" label="国家" show-overflow-tooltip class-name=".el-tooltip__popper">
      </el-table-column>
    </el-table>

    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 5px; font-size: 10px;">
      <ul class="pagination" v-html="pageString">
        
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MovieOverview',
  data() {
    return {
      movies: [],
      pageString: '',
      totalPages: 0,  // 总页码
      currentPage: 1,  // 默认页码
      searchPage: 1,   // 搜索框的页码
      searchKeys: '',  // 搜索关键字
    }
  },
  created() {
    this.initialData();
  },
  mounted() {
    console.log('电影信息表组件', this)
  },
  beforeDestroy() {
    console.log('电影信息表组件即将被销毁')
  },
  methods: {
    // 初始化数据
    async initialData() {
      await this.reqPage(this.currentPage)
    },
    async reqPage(page) {
      this.$axios
        .post("/userapi/movie_overview/", {
          page: page
        })
        .then((response) => {
          const data = response.data
          this.handleReturnData(data, page, 1)
        })
    },

    initialSearch() {
      this.search(1)
    },
    search(page) {
      console.log(this.searchKeys)
      if(this.searchKeys) {
        this.$axios
          .post("/userapi/search_movies/", {
            searchKeys: this.searchKeys,
            page: page
          })
          .then((response) => {
            const data = response.data
            this.handleReturnData(data, page, 2)
          })
      } else {
        alert('搜索关键字不能为空！')
      }
    },
    reset() {
      this.reqPage(1)
    },
    jump(who) {
      // 获取 input 元素
      const pageInput = document.querySelector('#pageInput');
      // 将 input 的值赋给 searchPage
      this.searchPage = pageInput.value;
      const pageNumber = parseInt(this.searchPage, 10);
      if (!isNaN(pageNumber) && pageNumber > 0 && pageNumber <= this.totalPages) {
        if (who === 1) {
          this.reqPage(pageNumber)
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
              this.reqPage(page)
            } else {
              this.search(page)
            }
          })
        })

        // 绑定搜索按钮事件
        const searchButton = document.querySelector('#searchButton')
        if (searchButton) {
          searchButton.addEventListener('click', () => {
            this.jump(who) // 这里传入参数 who
          })
        }
      })
    }
  },
}
</script>

<style>
.el-tooltip__popper{
  max-width:20%
}
</style>

<style scoped>
ul.pagination {
    margin: 10px 0 0 0;
}

ul.pagination li {display: inline;}

ul.pagination li a {
    color: black;
    float: left;
    padding: 8px 16px;
    text-decoration: none;
}
</style>