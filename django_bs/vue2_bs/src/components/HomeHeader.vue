<template>
  <div style="margin: 0;">
    <div class="navbar-header">
      <a class="navbar-brand" style="color: #fff">Vue+Django电影推荐+可视化</a>
    </div>

    <div v-if="username" class="dropdown collapse navbar-collapse" id="bs-example-navbar-collapse-1" style="float:right;">

      <button class="dropbtn nav navbar-nav navbar-right">{{ username}}</button>
      <div class="dropdown-content">
        <router-link to="/homepage/recommend">个人中心</router-link>
        <router-link to="/login">退出</router-link>
      </div>

      <!-- <ul class="nav navbar-nav navbar-right">
        <li>
            <router-link class="dropbtn">whh</router-link>
            <div class="dropdown-content">
              <router-link to="/homepage/recommend">个人中心</router-link>
              <hr />
              <router-link to="/login">退出</router-link>
            </div>
        </li>
      </ul> -->
    </div>
    <div v-else class="dropdown collapse navbar-collapse" id="bs-example-navbar-collapse-1" style="float:right;">
      <router-link to="/login" class="dropbtn nav navbar-nav navbar-right">登 录</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomeHeader",
  props: ['username'],
  /* mounted() {
    console.log('头部组件', this)
  }, */
};
</script>

<style scoped>
.dropbtn {
  background-color: #0c518e;
  color: white;
  text-align: center;
  text-decoration: none;
  width: 100px;
  height: 50px;
  border: none;
  cursor: pointer;
}
.dropdown {
    position: relative;
    display: inline-block;
}
.dropdown-content {
    display: none;
    position: absolute;
    background-color: #f9f9f9;
    width: 100px;
    margin-top: 50px;
    right: 0;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
}
.dropdown-content a {
    color: black;
    padding: 0px 16px;
    text-align: center;
    text-decoration: none;
    display: block;
}
.dropdown-content a:hover {background-color: #f1f1f1}

.dropdown:hover .dropdown-content {
    display: block;
}

.dropdown:hover .dropbtn {
    background-color: rgb(3, 3, 84);
}
</style>