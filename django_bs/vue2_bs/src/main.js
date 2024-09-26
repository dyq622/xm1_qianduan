import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import router from './router'
import ElementUI from 'element-ui'
// import Container from 'element-ui'
// import 'element-ui/lib/theme-chalk/index.css'
import axios from './axios'; // 引入axios
import store from './store'; // 引入 Vuex store


// axios.defaults.withCredentials = true  // 请求携带cookie
// axios.defaults.headers.post['X-CSRFToken'] = ''  //设置请求头的跨域密匙

// axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'

// axios.defaults.transformRequest = [function (data) {  //将发送的post参数封装成FROM-DATA，使后端接收
//   let ret = ''
//   for (let it in data) {
//     ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
//   }
//   return ret
// }];

// 将 axios 添加到 Vue 的原型上 
Vue.prototype.$axios = axios

Vue.config.productionTip = false
Vue.use(VueRouter)
Vue.use(ElementUI)
// Vue.prototype.$echarts = echarts
// Vue.use(Container)

new Vue({
  render: h => h(App),
  router: router,
  store: store
}).$mount('#app')
