// 引入打包可视化插件
const BundleAnalyzer = require('webpack-bundle-analyzer').BundleAnalyzerPlugin

const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  assetsDir: 'static',
  publicPath: './',
  configureWebpack: {
    externals: {
      'vue': 'Vue',
      'vue-router': 'VueRouter',
      'element-ui': 'ELEMENT',
      // 'echarts': 'echarts',
    },
    plugins: [
      new BundleAnalyzer()
    ]
  }
})
