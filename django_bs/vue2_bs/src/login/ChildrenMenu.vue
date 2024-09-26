<template>
  <el-row>
    <el-col>
      <el-menu
        class="el-menu-vertical-demo"
        background-color="#E9EEF3"
        text-color="black" router
      >
        <el-submenu index="1-1">
          <template slot="title">数据看板</template>
          <el-menu-item-group>
            <el-menu-item index="/dashboard">数据看板</el-menu-item>
            <el-menu-item index="/movie_overview">电影概况</el-menu-item>
            <el-menu-item index="/review_overview">短评概况</el-menu-item>
          </el-menu-item-group>
        </el-submenu>

        <el-submenu index="1-2">
          <template slot="title">用户管理</template>
          <el-menu-item-group>
            <el-menu-item index="/user_center">个人中心</el-menu-item>
            <el-menu-item index="/update_psw">修改密码</el-menu-item>
          </el-menu-item-group>
        </el-submenu>

        <el-submenu index="1-3">
          <template slot="title">分析</template>
          <el-menu-item-group>
            <el-menu-item index="/type_analysis">电影类型分析</el-menu-item>
            <el-menu-item index="/duration_analysis">运行时长分析</el-menu-item>
            <el-menu-item index="/country_analysis">电影国家分析</el-menu-item>
            <el-menu-item index="/language_analysis">电影语种分析</el-menu-item>
            <el-menu-item index="/high_frequency_actor">高频演员</el-menu-item>
          </el-menu-item-group>
        </el-submenu>

        <el-submenu index="1-4">
          <template slot="title">评论分析</template>
          <el-menu-item-group>
            <el-menu-item index="/all_board">整体看板</el-menu-item>
            <el-menu-item index="/good_view">好评分析</el-menu-item>
            <el-menu-item index="/middle_view">中评分析</el-menu-item>
            <el-menu-item index="/bad_view">差评分析</el-menu-item>
          </el-menu-item-group>
        </el-submenu>

        <el-submenu index="1-5">
          <template slot="title">特征词模型</template>
          <el-menu-item-group>
            <el-menu-item index="/textrank">TextRank</el-menu-item>
          </el-menu-item-group>
        </el-submenu>

      </el-menu>
    </el-col>
  </el-row>
</template>

<script>
export default {
  naem: 'ChildrenMenu'
}
</script>

<style>
  
</style>

