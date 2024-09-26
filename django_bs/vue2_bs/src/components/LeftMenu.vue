<template>
  <el-menu text-color="black" :unique-opened="true" router>
    <el-submenu index="1">
      <template slot="title">核心功能</template>
      <el-menu-item-group>
        <el-menu-item index="/homepage/movie_library">电影库</el-menu-item>
        <el-menu-item index="/homepage/movie_recommend">电影推荐</el-menu-item>
      </el-menu-item-group>
    </el-submenu>

    <el-submenu index="2">
      <template slot="title">数据面板</template>
      <el-menu-item-group>
        <el-menu-item index="/homepage/movie_data_tongji">电影数据统计</el-menu-item>
        <el-menu-item index="/homepage/short_comment_data_tongji">短评数据统计</el-menu-item>
        <el-menu-item index="/homepage/film_review_data_tongji">影评数据统计</el-menu-item>

        <el-menu-item index="/homepage/movie_overview">电影信息表</el-menu-item>
        <el-menu-item index="/homepage/short_comment_overview">短评信息表</el-menu-item>
        <el-menu-item index="/homepage/film_review_overview">影评信息表</el-menu-item>
      </el-menu-item-group>
    </el-submenu>

    <el-submenu index="3">
      <template slot="title">电影分析</template>
      <el-menu-item-group>
        <el-menu-item index="/homepage/type_analysis">电影类型分析</el-menu-item>
        <el-menu-item index="/homepage/country_analysis">电影国家分析</el-menu-item>
        <el-menu-item index="/homepage/high_frequency_actor">高频演员</el-menu-item>
      </el-menu-item-group>
    </el-submenu>

    <el-submenu index="4">
      <template slot="title">短评分析</template>
      <el-menu-item-group>
        <el-menu-item index="3-2">好评分析</el-menu-item>
        <el-menu-item index="3-3">中评分析</el-menu-item>
        <el-menu-item index="3-4">差评分析</el-menu-item>
      </el-menu-item-group>
    </el-submenu>

    <el-submenu index="5">
      <template slot="title">影评分析</template>
      <el-menu-item-group>
        <el-menu-item index="3-2">好评分析</el-menu-item>
        <el-menu-item index="3-3">中评分析</el-menu-item>
        <el-menu-item index="3-4">差评分析</el-menu-item>
      </el-menu-item-group>
    </el-submenu>

    <el-submenu index="6">
      <template slot="title">特征词模型</template>
      <el-menu-item-group>
        <el-menu-item index="4-1">TextRank</el-menu-item>
      </el-menu-item-group>
    </el-submenu>

    <el-submenu index="7">
      <template slot="title">用户管理</template>
      <el-menu-item-group>
        <el-menu-item index="5-1">个人中心</el-menu-item>
        <el-menu-item index="5-2">修改密码</el-menu-item>
      </el-menu-item-group>
    </el-submenu>
  </el-menu>
</template>

<script>
export default {
  name: "LeftMenu",
};
</script>

<style scoped>
/* 使父菜单项背景色为蓝色 */
.el-menu {
  background-color: #5aa9f8;
}

/* 使子菜单项背景色为浅蓝色 */
.el-menu .el-submenu__title {
  background-color: #58a8f8; /* 浅蓝色背景 */
}

/* 确保子菜单项在展开时保持浅蓝色背景 */
.el-menu .el-submenu.is-opened .el-menu {
  background-color: #58a8f8; /* 浅蓝色背景 */
}

/* 使子菜单项的 hover 状态也保持浅蓝色背景 */
.el-menu .el-menu-item:hover {
  background-color: #7ab2eb;
}
</style>