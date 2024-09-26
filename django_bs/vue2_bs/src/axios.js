import axios from 'axios';

axios.defaults.withCredentials = true;  // 请求携带cookie
axios.defaults.headers.post['X-CSRFToken'] = '';  // 设置请求头的跨域密钥
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

axios.defaults.transformRequest = [function (data) {  // 将发送的post参数封装成FORM-DATA
  let ret = '';
  for (let it in data) {
    ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&';
  }
  return ret;
}];

export default axios;