<template>
  <div id="app">
    <keep-alive include="HomePage">
      <router-view ></router-view>
    </keep-alive>
  </div>
</template>

<script>
  export default {
    name: "App",
  }
</script>

<style scoped>

</style>