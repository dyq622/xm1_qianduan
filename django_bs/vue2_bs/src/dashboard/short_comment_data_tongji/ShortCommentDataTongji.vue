<template>
  <el-container style="border: 2px solid #eee;">
    <el-header style="height: 20px;">
      <span style="color: #008000; font-size: 16px;">短评数据统计</span>
    </el-header>
    <el-main>
      <div style="margin-bottom: 5px;">
        <el-row :gutter="20">
          <el-col :span="4" v-for="(value, title) in statistics" :key="title">
            <div>
              <el-statistic :title="title" :value="value" group-separator="," default-value="0"></el-statistic>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-main>
  </el-container>
</template>

<!-- <script>
export default {
  name: 'ShortCommentDataTongji',
  data() {
    return {
      totalCommentNumber: 0,
      highRecommend: 0,
      middleRecommend: 0,
      generalRecommend: 0,
      poor: 0,
      bad: 0,
    }
  },
  computed: {
    statistics() {
      return {
        '短评总数': this.totalCommentNumber,
        '力荐': this.highRecommend,
        '推荐': this.middleRecommend,
        '还行': this.generalRecommend,
        '较差': this.poor,
        '很差': this.bad,
      };
    },
  },
  created() {
    this.reqInitialData()  // html加载完成前向后台请求数据
  },
  mounted() {
    console.log('统计短评数据组件', this);
  },
  methods: {
    async reqInitialData() {
      await this.reqData()
    },
    async reqData() {
      this.$axios
        .get("/userapi/short_comment_data_tongji/")
        .then((response) => {
          const data = response.data
          this.totalCommentNumber = data.totalCommentNumber
          this.highRecommend = data.highRecommend
          this.middleRecommend = data.middleRecommend
          this.generalRecommend = data.generalRecommend
          this.poor = data.poor
          this.bad = data.bad
        })
    }
  },
}
</script> -->


<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'ShortCommentDataTongji',
  created() {
    this.reqInitialData();
    console.log('统计短评数据', this);
  },
  computed: {
    ...mapGetters('shortCommentDashBoard', [
      'totalCommentNumber',
      'highRecommend',
      'middleRecommend',
      'generalRecommend',
      'poor',
      'bad',
    ]),
    statistics() {
      return {
        '短评总数': this.totalCommentNumber,
        '力荐': this.highRecommend,
        '推荐': this.middleRecommend,
        '还行': this.generalRecommend,
        '较差': this.poor,
        '很差': this.bad,
      };
    },
  },
  methods: {
    ...mapActions('shortCommentDashBoard', {
      fetchData: 'fetchData',
    }),
    async reqInitialData() {
      await this.fetchData(this);
    },
  },
};
</script>

<style>
/* 这里可以添加样式 */
</style>