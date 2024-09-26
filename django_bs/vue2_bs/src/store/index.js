import Vue from 'vue';
import Vuex from 'vuex';

import shortCommentDashBoard from './modules/shortCommentDashBoard';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    shortCommentDashBoard,
  },
});