<template>
  <el-container style="height: calc(100vh);">
    <el-header style="height: 50px; position: fixed; top: 0; left: 0; right: 0; z-index: 100;">
      <HomeHeader :username="username" />
    </el-header>
    <el-container style="padding-top: 50px;">
      <el-aside width="215px" style="position: fixed; top: 50px; bottom: 0; overflow-y: auto;">
        <!--引入自定义左侧菜单栏-->
        <left-menu></left-menu>
      </el-aside>
      <el-main style="margin-left: 215px; padding: 5px; height: calc(100vh - 50px); overflow-y: auto;">
        <!--引入跳转路由-->
        <keep-alive :include="cachedComponents">
          <router-view></router-view>
        </keep-alive>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import HomeHeader from './HomeHeader'
import LeftMenu from './LeftMenu'

export default {
  name: 'HomePage',
  components: {
    HomeHeader,
    LeftMenu
  },
  data() {
    return {
      username: '',
      cachedComponents: [
        'MovieLibrary', 'MovieRecommend', 'MovieDashBoard', 'MovieOverview', 'ShortCommentOverview', 'CountryAnalysis', 'TypeAnalysis', 'HighFreActor'
      ]
    }
  },
  created() {
    this.username = this.$route.query.username
  },
  mounted() {
    console.log('主页组件', this)
  },
  beforeDestroy() {
    console.log('主页组件即将被销毁')
  },
}
</script>

<style scoped>
.el-header {
  background-color: #0c518e;
  color: #333;
  /* height: 50px; */
  /* text-align: center; */
  line-height: 50px;
}
.el-aside {
  background-color: #0c518e;
  color: #333;
}
/* body > .el-container {
  margin-bottom: 40px;
} */
</style>