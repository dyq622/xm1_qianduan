import VueRouter from 'vue-router'

import HomePage from '../components/HomePage'

import BsLogin from '../login/BsLogin'  //导入login组件
import BsRegister from '../login/BsRegister' //导入register组件

// 核心功能————电影库、电影推荐
import MovieLibrary from '../core_function/MovieLibrary'
import MovieRecommend from '../core_function/MovieRecommend'

// 数据面板————电影数据统计、短评数据统计、影评数据统计、电影信息表、短评信息表、影评信息表
import MovieDashBoard from '../dashboard/movie_data_tongji/MovieDashBoard'
import ShortCommentDashBoard from '../dashboard/short_comment_data_tongji/ShortCommentDashBoard'
import FilmReviewDashBoard from '../dashboard/film_review_data_tongji/FilmReviewDashBoard'
import MovieOverview from '../dashboard/MovieOverview'
import ShortCommentOverview from '../dashboard/ShortCommentOverview' 
import FilmReviewOverview from '../dashboard/FilmReviewOverview'

// 电影分析————电影类型分析、电影国家分析、高频演员
import TypeAnalysis from '../analysis/TypeAnalysis'
import CountryAnalysis from '../analysis/CountryAnalysis'
import HighFreActor from '../analysis/HighFreActor'

// 用户管理————个人中心、修改密码
import UserCenter from '../user_management/UserCenter'
import UpdatePassword from '../user_management/UpdatePassword' 

// 评论分析————整体概况、好评分析、中评分析、差评分析
import AllBoard from '../comment_analysis/AllBoard'
import GoodView from '../comment_analysis/GoodView'
import MiddleView from '../comment_analysis/MiddleView'
import BadView from '../comment_analysis/BadView'

// 特征词模型————TextRank
import TextRank from '../feature_word/TextRank'

//配置组件及路径的对应关系
const routes = [
  {
    path: '/',
    redirect: '/login' // 默认情况下重定向到登录页面
  },
  {
    name: 'BsLogin',
    path: '/login',
    component: BsLogin,
    meta: { title: '登录页面' }
  },
  {
    name: 'Register',
    path: '/register',
    component: BsRegister,
    meta: { title: '注册页面' }
  },

  {
    name: 'HomePage',
    path: '/homepage',
    component: HomePage,
    meta: { title: '推荐系统+可视化' },
    props( $route ) {
      return { 
        username: $route.query.username, 
      }
    },
    children: [
      {
        name: 'MovieLibrary',
        path: 'movie_library',
        component: MovieLibrary,
        meta: { title: '电影库' }
      },
      {
        name: 'MovieRecommend',
        path: 'movie_recommend',
        component: MovieRecommend,
        meta: { title: '电影推荐' }
      },

      {
        name: 'MovieDashBoard',
        path: 'movie_data_tongji',
        component: MovieDashBoard,
        meta: { title: '电影数据统计' }
      },
      {
        name: 'ShortCommentDashBoard',
        path:'short_comment_data_tongji',
        component: ShortCommentDashBoard,
        meta: { title: '短评数据统计' }
      },
      {
        name: 'FilmReviewDashBoard',
        path: 'film_review_data_tongji',
        component: FilmReviewDashBoard,
        meta: { title: '影评数据统计' }
      },
      {
        name: 'MovieOverview',
        path: 'movie_overview',
        component: MovieOverview,
        meta: { title: '电影信息表' }
      },
      {
        name: 'ShortCommentOverview',
        path: 'short_comment_overview',
        component: ShortCommentOverview,
        meta: { title: '短评信息表' }
      },
      {
        name: 'FilmReviewOverview',
        path: 'film_review_overview',
        component: FilmReviewOverview,
        meta: { title: '影评信息表' }
      },

      {
        name: 'TypeAnalysis',
        path: 'type_analysis',
        component: TypeAnalysis,
        meta: { title: '电影类型分析' }
      },
      {
        name: 'CountryAnalysis',
        path: 'country_analysis',
        component: CountryAnalysis,
        meta: { title: '电影国家/地区分析' }
      },
      {
        name: 'HighFreActor',
        path: 'high_frequency_actor',
        component: HighFreActor,
        meta: { title: '高频演员' }
      },
    ]
  },
  

  {
    name: 'AllBoard',
    path: '/all_board',
    component: AllBoard,
    meta: { title: '整体看板' }
  },
  {
    name: 'GoodView',
    path: '/good_view',
    component: GoodView,
    meta: { title: '好评分析' }
  },
  {
    name: 'MiddleView',
    path: '/middle_view',
    component: MiddleView,
    meta: { title: '中评分析' }
  },
  {
    name: 'BadView',
    path: '/bad_view',
    component: BadView,
    meta: { title: '差评分析' }
  },

  {
    name: 'TextRank',
    path: '/textrank',
    component: TextRank,
    meta: { title: '特征词模型' }
  },

  {
    name: 'UserCenter',
    path: '/user_center',
    component: UserCenter,
    meta: { title: '个人中心' }
  },
  {
    name: 'UpdatePassword',
    path: '/update_psw',
    component: UpdatePassword,
    meta: { title: '修改密码' }
  },
]

const router = new VueRouter({
  // history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  if (to.meta.isAuth) {  // 判断是否需要鉴权
    if (localStorage.getItem('name') === 'whh') {
      next()
    } else {
      alert('无权限查看')
    }
  } else {
    next()
  }
})

router.afterEach((to) => {
  document.title = to.meta.title || 'whh毕设'
})

export default router //将路由配置导出