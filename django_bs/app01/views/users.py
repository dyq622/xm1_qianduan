# from django.http import JsonResponse
# import csv

from django.http import JsonResponse
from app01.models import MovieUser, MovieInfo, MovieDetails, MovieShortComment, SimilarMovies
from app01.utils.pagination import Pagination
# from app01 import models
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
# from rest_framework.request import Request
from django.db.models import Q
from django.db.models import Avg, Sum
from collections import Counter
from datetime import datetime

import requests
from lxml import etree


class ApiUser(viewsets.ViewSet):
    # 只有两个参数，默认路由后缀为方法名，可以添加第三个参数url_path='login'指定

    # 登录注册
    @action(methods=['post'], detail=False)
    def login(self, request):
        # 对象使用.获取，字典使用['key']获取
        password = MovieUser.objects.filter(username=request.data['username']).first().password
        result = {
            "code": 200,
            "msg": "用户登录成功！",
            "body": ""
        }
        if password == request.data['password']:
            return Response(result)
        else:
            result['msg'] = "用户名或密码错误！"
            result['code'] = -1
            return Response(result)
    
    @action(methods=['post'], detail=False)
    def register(self, request):
        username = request.data['username']
        password = request.data['password']
        MovieUser.objects.create(username=username, password=password)
        result = {
            "code": 200,
            "msg": "用户注册成功！",
            "body": ""
        }
        return Response(result)
    
    # 电影信息表
    @action(methods=['post'], detail=False)
    def movie_overview(self, request):
        # 从查询参数中获取页码，默认为1
        page_number = int(request.data['page'])
        queryset = MovieInfo.objects.all()
        page_object = Pagination(queryset, 11, page_number)  # 每页8条数据
        
        data = {
            "movies": list(page_object.page_queryset.values(
                'movieName', 'releaseInfo', 'movieScoring', 'commentNumber', 
                'mainActor', 'movieType', 'movieCountry', 'movieID'
            )),  # 转换为 JSON 可序列化的格式
            "total_pages": page_object.total_page_count,  # 总页码
            "page_string": page_object.html()  # 页码 HTML
        }
        
        return JsonResponse(data)
    
    @action(methods=['post'], detail=False)
    def search_movies(self, request):
        search_keys = request.data['searchKeys']
        page = int(request.data['page'])
        # 创建一个查询集
        queryset = MovieInfo.objects.all()
        

        # 如果有搜索关键字字符串，进行过滤
        if search_keys:
            # 将搜索关键字字符串分割成多个关键字
            keys = search_keys.split()  # 默认按空格分割，如果有其他分隔符，可以修改这里

            # 创建查询条件
            query = Q()
            for key in keys:
                # 在所有列上进行模糊匹配
                query |= Q(movieName__icontains=key) | \
                        Q(releaseInfo__icontains=key) | \
                        Q(movieScoring__icontains=key) | \
                        Q(commentNumber__icontains=key) | \
                        Q(mainActor__icontains=key) | \
                        Q(movieType__icontains=key) | \
                        Q(movieCountry__icontains=key)

            # 应用查询条件到查询集
            queryset = queryset.filter(query)
            page_object = Pagination(queryset, 11, page)  # 每页8条数据
            data = {
                "movies": list(page_object.page_queryset.values(
                    'movieName', 'releaseInfo', 'movieScoring', 'commentNumber',
                    'mainActor', 'movieType', 'movieCountry', 'movieID'
                )),  # 转换为 JSON 可序列化的格式
                "total_pages": page_object.total_page_count,  # 总页码
                "page_string": page_object.html()  # 页码 HTML
            }
            
            return JsonResponse(data)

    # 短评信息表
    @action(methods=['post'], detail=False)
    def short_comments(self, request):
        # 从查询参数中获取页码，默认为1
        page_number = int(request.data['page'])
        queryset = MovieShortComment.objects.all()
        page_object = Pagination(queryset, 11, page_number)  # 每页8条数据
        
        data = {
            "comments": list(page_object.page_queryset.values(
                'movieName', 'commentPerson', 'ratingScale',
                'commentDate', 'starNumber', 'commentContent'
            )),  # 转换为 JSON 可序列化的格式
            "total_pages": page_object.total_page_count,  # 总页码
            "page_string": page_object.html()  # 页码 HTML
        }
        
        return JsonResponse(data)
    
    @action(methods=['post'], detail=False)
    def search_shortcomments(self, request):
        search_keys = request.data['searchKeys']
        page = int(request.data['page'])
        # 创建一个查询集
        queryset = MovieShortComment.objects.all()
        

        # 如果有搜索关键字字符串，进行过滤
        if search_keys:
            # 将搜索关键字字符串分割成多个关键字
            keys = search_keys.split()  # 默认按空格分割，如果有其他分隔符，可以修改这里

            # 创建查询条件
            query = Q()
            for key in keys:
                # 在所有列上进行模糊匹配
                query |= Q(movieName__icontains=key) | \
                        Q(commentPerson__icontains=key) | \
                        Q(ratingScale__icontains=key) | \
                        Q(commentDate__icontains=key) | \
                        Q(starNumber__icontains=key) | \
                        Q(commentContent__icontains=key)

            # 应用查询条件到查询集
            queryset = queryset.filter(query)
            page_object = Pagination(queryset, 11, page)  # 每页8条数据
            data = {
                "comments": list(page_object.page_queryset.values(
                    'movieName', 'commentPerson', 'ratingScale',
                    'commentDate', 'starNumber', 'commentContent'
                )),  # 转换为 JSON 可序列化的格式
                "total_pages": page_object.total_page_count,  # 总页码
                "page_string": page_object.html()  # 页码 HTML
            }
            
            return JsonResponse(data)
        
    # 电影数据统计
    @action(methods=['get'], detail=False)
    def movie_data_tongji(self, request):
        queryset1 = MovieInfo.objects.all()
        # 计算电影总数和平均评分和评论总数
        total_movies = queryset1.count()
        # aggregate 返回一个字典，其中 rating__avg 是平均评分的键。
        average_rating = queryset1.aggregate(Avg('movieScoring'))['movieScoring__avg']
        total_commentPeopleNumber = queryset1.aggregate(Sum('commentNumber'))['commentNumber__sum']

        # 准备响应数据
        data = {
            "total_movies": total_movies,  # 电影总数
            "average_rating": average_rating,  # 平均评分
            "total_commentPeopleNumber": total_commentPeopleNumber,  # 总评论人数
        }
        
        return Response(data)
    
    @action(methods=['get'], detail=False)
    def movie_data_report(self, request):
        # 从数据库中获取所有 releaseInfo 数据
        queryset = MovieInfo.objects.values_list('releaseInfo', flat=True)

        # 统计每年出现的次数
        year_counts = {}
        
        for release_info in queryset:
            try:
                # 将字符串转换为日期并提取年份
                year = datetime.strptime(release_info, '%Y-%m-%d').year
                year_counts[year] = year_counts.get(year, 0) + 1
            except ValueError:
                # 处理无效日期格式的情况
                pass

        # 将年份按升序排序
        sorted_years = sorted(year_counts.keys())
        sorted_year_counts = [year_counts[year] for year in sorted_years]

        # 准备响应数据
        data = {
            "years": sorted_years,         # 所有年份的列表
            "year_data": sorted_year_counts # 对应年份的电影总数
        }

        """ # 定义时间区间
        intervals = [(1920, 1930), (1931, 1940), (1941, 1950), (1951, 1960), 
                     (1961, 1970), (1971, 1980), (1981, 1990), (1991, 2000), 
                     (2001, 2010), (2011, 2020), (2021, 2024)]
        
        # 统计每个时间区间的电影数量
        interval_counts = {f"{start}-{end}": 0 for start, end in intervals}
        
        for year, count in year_counts.items():
            for start, end in intervals:
                if start <= year <= end:
                    interval_counts[f"{start}-{end}"] += count
                    break
        
        # 准备响应数据
        sorted_intervals = sorted(interval_counts.keys())
        sorted_counts = [interval_counts[interval] for interval in sorted_intervals]

        data = {
            "years": sorted_intervals,    # 时间区间列表
            "year_data": sorted_counts   # 对应时间区间的电影总数
        } """

        return Response(data)
    
    @action(methods=['get'], detail=False)
    def high_score_films(self, request):
        # 查询评分最高和评论人数最多的前15部电影
        queryset = MovieInfo.objects.all().order_by('-movieScoring', '-commentNumber')[:15]
        
        # 转换为 JSON 可序列化的格式
        data = {
            "movies": list(queryset.values(
                'movieName', 'movieType'
            )),
        }
        
        return Response(data)
    
    # 短评数据统计
    @action(methods=['get'], detail=False)
    def short_comment_data_tongji(self, request):
        queryset = MovieShortComment.objects.all()
        # 计算短评总数
        total_comment_number = queryset.count()

        # 统计每个评分等级的数量
        high_recommend = queryset.filter(ratingScale='力荐').count()
        middle_recommend = queryset.filter(ratingScale='推荐').count()
        general_recommend = queryset.filter(ratingScale='还行').count()
        poor = queryset.filter(ratingScale='较差').count()
        bad = queryset.filter(ratingScale='很差').count()

        # 将数据合并
        data = {
            "totalCommentNumber": total_comment_number,
            "highRecommend": high_recommend,
            "middleRecommend": middle_recommend,
            "generalRecommend": general_recommend,
            "poor": poor,
            "bad": bad,
        }

        return Response(data)


    # 电影类型分析
    @action(methods=['get'], detail=False)
    def movie_type(self, request):
        queryset = MovieInfo.objects.all()
        
        # 初始化类型统计字典
        type_counter = Counter()

        # 遍历每部电影的类型
        for movie in queryset:
            # 分割电影类型字符串并更新计数器
            types = movie.movieType.split(',')  # 使用 '，' 分隔类型
            type_counter.update(types)

        # 转换为列表格式
        type_num = [{"value": value, "name": key} for key, value in type_counter.items()]
        
        # 获取所有电影类型的列表
        movie_type = list(type_counter.keys())
        
        # 获取每种类型的电影总数
        movie_type_num = [type_counter[type] for type in movie_type]

        data = {
            "type_num": type_num,
            "movie_type": movie_type,
            "movie_type_num": movie_type_num,
        }

        return Response(data)

    # 制片国家/地区分析
    @action(methods=['get'], detail=False)
    def country_type(self, request):
        queryset = MovieInfo.objects.all()
        
        # 初始化类型统计字典
        type_counter = Counter()

        # 遍历每部电影
        for movie in queryset:
            # 分割国家/地区字符串并更新计数器
            types = movie.movieCountry.split(',')  # 使用 ',' 分隔类型
            type_counter.update(types)

        # 过滤掉数量小于10的国家/地区
        filtered_counter = {key: value for key, value in type_counter.items() if value >= 5}

        # 转换为列表格式
        type_num = [{"value": value, "name": key} for key, value in filtered_counter.items()]
        
        # 获取所有国家/地区的列表
        country_type = list(filtered_counter.keys())
        
        # 获取每种类型的电影总数
        country_type_num = [filtered_counter[type] for type in country_type]

        data = {
            "type_num": type_num,
            "country_type": country_type,
            "country_type_num": country_type_num,
        }

        return Response(data)

    # 高频演员
    @action(methods=['get'], detail=False)
    def high_freActor(self, request):
        queryset = MovieInfo.objects.all()
        
        # 初始化类型统计字典
        actor_counter = Counter()

        # 遍历每部电影
        for movie in queryset:
            # 分割主要演员字符串并更新计数器
            types = movie.mainActor.split(',')  # 使用 ',' 分隔类型
            actor_counter.update(types)

        # 过滤掉当过主演次数小于5的演员
        filtered_counter = {key: value for key, value in actor_counter.items() if value >= 5}

        # 转换为列表格式
        actor_num = [{"name": key, "value": value} for key, value in filtered_counter.items()]

        data = {
            "actor_num": actor_num,
        }

        return Response(data)

    # 电影库
    @action(methods=['post'], detail=False)
    def movie_library(self, request):
        page_number = int(request.data['page'])
        queryset = MovieDetails.objects.all().order_by('-movieScoring', '-commentNumber')
        page_object = Pagination(queryset, 8, page_number, 2)  # 每页8条数据

        # 转换为 JSON 可序列化的格式
        data = {
            'movies': list(page_object.page_queryset.values(
                'movieName', 'imageUrl', 'movieScoring', 'commentNumber', 'movieType', 'releaseInfo',
                'duration', 'director', 'actors', 'movieCountry', 'languages', 'introduction'
            )),
            'total_pages': page_object.total_page_count,  # 总页码
            'page_string': page_object.html()  # 页码 HTML
        }
        
        return Response(data)
        
    @action(methods=['post'], detail=False)
    def search_movie_library(self, request):
        search_keys = request.data['search_keys']
        page = int(request.data['page'])
        queryset = MovieDetails.objects.all()

        # 如果有搜索关键字字符串，进行过滤
        if search_keys:
            # 将搜索关键字字符串分割成多个关键字
            keys = search_keys.split()  # 默认按空格分割，如果有其他分隔符，可以修改这里

            # 创建查询条件
            query = Q()
            for key in keys:
                # 在所有列上进行模糊匹配
                query |= Q(movieName__icontains=key) | \
                        Q(imageUrl__icontains=key) | \
                        Q(movieScoring__icontains=key) | \
                        Q(commentNumber__icontains=key) | \
                        Q(movieType__icontains=key) | \
                        Q(releaseInfo__icontains=key) | \
                        Q(duration__icontains=key) | \
                        Q(director__icontains=key) | \
                        Q(actors__icontains=key) | \
                        Q(movieCountry__icontains=key) | \
                        Q(languages__icontains=key) | \
                        Q(introduction__icontains=key)

            # 应用查询条件到查询集
            queryset = queryset.filter(query)
            page_object = Pagination(queryset, 8, page, 2)  # 每页8条数据
            data = {
                'movies': list(page_object.page_queryset.values(
                    'movieName', 'imageUrl', 'movieScoring', 'commentNumber', 'movieType', 'releaseInfo',
                    'duration', 'director', 'actors', 'movieCountry', 'languages', 'introduction'
                )),
                'total_pages': page_object.total_page_count,  # 总页码
                'page_string': page_object.html()  # 页码 HTML
            }
        
            return Response(data)
        
    # 电影推荐
    @action(methods=['post'], detail=False)
    def movie_recommend(self, request):
        searchMovieName = request.data['searchMovieName']
        page = int(request.data['page'])

        # Step 1: 查找SimilarMovies表中searchMovieName对应的记录
        try:
            similar_movies_entry = SimilarMovies.objects.get(movieName=searchMovieName)
        except SimilarMovies.DoesNotExist:
            data = {
                'code': 404,
                'msg': '本系统没有该电影或没有该电影的推荐',
            }
            return Response(data)

        # Step 2: 从similarMovies列中取出前16个相似电影名称
        similar_movies_list = similar_movies_entry.similarMovies.split(',')
        top_16_movies = similar_movies_list[:16]

        # Step 3: 从MovieDetails表中获取这些电影的详细信息
        queryset = MovieDetails.objects.all()

        # Step 4: 创建查询条件
        query = Q()
        for movie in top_16_movies:
            # 在所有列上进行模糊匹配
            query |= Q(movieName__icontains=movie)

        # 应用查询条件到查询集
        queryset = queryset.filter(query)[:16]
        page_object = Pagination(queryset, 4, page, 1)  # 每页8条数据,第1页

        # Step 5: 转换为 JSON 可序列化的格式
        data = {
            'code': 200,
            'msg': '查询成功!',
            'movies': list(page_object.page_queryset.values(
                'movieName', 'imageUrl', 'movieScoring', 'commentNumber', 'movieType', 'releaseInfo',
                'duration', 'director', 'actors', 'movieCountry', 'languages', 'introduction'
            )),
            'total_pages': page_object.total_page_count,  # 总页码
            'page_string': page_object.html()  # 页码 HTML
        }
        
        return Response(data)