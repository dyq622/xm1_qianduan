"""
自定义的分页组件，以后如果想要使用这个分页组件，你需要做如下几件事：

在视图函数中：
    def pretty_list(request):

        # 1、根据自己的情况去筛选自己的数据
        queryset = PrettyNum.objects.all()

        # 2、实例化分页对象
        page_object = Pagination(request, queryset)

        context = {
            "queryset": page_object.page_queryset,  # 分完页的数据
            "page_string": page_object.html()       # 页码
        }

        return render(request, "pretty_list.html", context)

在html页面中：
    {% for obj in queryset %}
        {{ obj.xx }}
    {% endfor %}

    <ul class="pagination">
        {{ page_string }}
    </ul>

"""

from django.utils.safestring import mark_safe


class Pagination(object):

    def __init__(self, queryset, page_size=7, page=1, plus=3):
        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据（根据这个数据给他进行分页处理）
        :param page_size: 每页显示多少条数据
        :param plus: 显示当前页的 前或后几页（页码）
        """

        # from django.http.request import QueryDict
        # import copy
        # query_dict = copy.deepcopy(request.GET)
        # query_dict._mutable = True
        # self.query_dict = query_dict

        # self.page_param = page_param
        # page = request.GET.get(page_param, "1")
        # if page.isdecimal():
        #     page = int(page)
        # else:
        #     page = 1

        self.page = page
        self.page_size = page_size

        self.start = (page-1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        # 数据的总条数
        total_count = queryset.count()

        # 总页码
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        # 计算出，显示当前页的前3页、后3页
        if self.total_page_count <= 2 * self.plus + 1:
            # 数据库中的数据比较少，没有达到7页
            start_page = 1
            end_page = self.total_page_count
        else:
            # 数据库中的数据比较多 > 7页

            # 当前页<5时(小jizhi)
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # 当前页 > 3
                # 当前页 + 3 > 总页面
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码
        page_str_list = []

        # 首页
        page_str_list.append('<li><a data-page="{}">首页</a></li>'.format(1))

        # 上一页
        if self.page > 1:
            prev = '<li><a data-page="{}">上一页</a></li>'.format(self.page - 1)
        else:
            prev = '<li><a data-page="{}">上一页</a></li>'.format(1)
        page_str_list.append(prev)

        for i in range(start_page, end_page + 1):
            if i == self.page:
                ele = '<li class="active"><a data-page="{}">{}</a></li>'.format(i, i)
            else:
                ele = '<li><a data-page="{}">{}</a></li>'.format(i, i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            next_page = '<li><a data-page="{}">下一页</a></li>'.format(self.page + 1)
        else:
            next_page = '<li><a data-page="{}">下一页</a></li>'.format(self.total_page_count)
        page_str_list.append(next_page)

        # 尾页
        page_str_list.append('<li><a data-page="{}">尾页</a></li>'.format(self.total_page_count))

        search_string = """
            <li>
                <input id="pageInput" style="width: 45.33px; height: 27.61px;" type="text" placeholder="页码">
                <button id="searchButton" style="width: 45.33px; height: 27.61px; margin-left: -4px" class="btn-primary" @click="search">跳转</button>
            </li>
        """

        page_str_list.append(search_string)

        page_string = mark_safe("".join(page_str_list))
        return page_string
