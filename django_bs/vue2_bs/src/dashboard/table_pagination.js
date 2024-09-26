export function pagination(this, data, page, fetchPage, jump) {
  // 更新页面内容
  this.movies = data.movies;
  this.pageString = data.page_string;
  this.totalPages = data.total_pages;
  this.currentPage = page;

  // 使用 $nextTick 确保 DOM 已更新
  this.$nextTick(() => {
    // 绑定事件到分页链接
    document.querySelectorAll('.pagination a').forEach(link => {
      link.addEventListener('click', (event) => {
        event.preventDefault();
        const page = parseInt(event.target.getAttribute('data-page'), 10);
        fetchPage(page);
      });
    });

    // 绑定搜索按钮事件
    const searchButton = document.querySelector('#searchButton');
    if (searchButton) {
      searchButton.addEventListener('click', jump);
    }
  })
}