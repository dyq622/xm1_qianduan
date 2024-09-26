// import axios from '../../axios';

const state = {
  totalCommentNumber: 0,   // 短评总数
  highRecommend: 0,         // 力荐
  middleRecommend: 0,       // 推荐
  generalRecommend: 0,      // 还行
  poor: 0,                  // 较差
  bad: 0                    // 很差
};

const mutations = {
  SET_DATA(state, data) {
    state.totalCommentNumber = data.totalCommentNumber || 0;
    state.highRecommend = data.highRecommend || 0;
    state.middleRecommend = data.middleRecommend || 0;
    state.generalRecommend = data.generalRecommend || 0;
    state.poor = data.poor || 0;
    state.bad = data.bad || 0;
  },
};

const actions = {
  fetchData(context, value) {
    console.log('请求统计的短评数据');
    value.$axios.get('/userapi/short_comment_data_tongji/')
    .then(response => {
      context.commit('SET_DATA', response.data);
    })
  },
};

const getters = {
  totalCommentNumber: (state) => state.totalCommentNumber,
  highRecommend: (state) => state.highRecommend,
  middleRecommend: (state) => state.middleRecommend,
  generalRecommend: (state) => state.generalRecommend,
  poor: (state) => state.poor,
  bad: (state) => state.bad,
};

export default {
  state,
  mutations,
  actions,
  getters,
};