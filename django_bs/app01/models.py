from django.db import models

# Create your models here.

# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver 127.0.0.1:8080
# 在终端修改编码：
# ALTER TABLE app01_movieshortcomment MODIFY COLUMN commentPerson VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
# ALTER TABLE app01_movieshortcomment MODIFY COLUMN commentContent TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
# 重置数据表：TRUNCATE TABLE app01_movieinfo;

class MovieUser(models.Model):
    """ 登录用户表 """
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)

    def __str__(self):
        return self.username
    

class MovieInfo(models.Model):
    """ 电影信息表 """
    movieName = models.CharField(verbose_name='电影名', max_length=64)
    releaseInfo = models.CharField(verbose_name='上映日期', max_length=64)
    movieScoring = models.DecimalField(verbose_name='评分', max_digits=3, decimal_places=1)
    commentNumber = models.IntegerField(verbose_name='评论人数')
    mainActor = models.CharField(verbose_name='主要演员', max_length=256)
    movieType = models.CharField(verbose_name='类型', max_length=128)
    movieCountry = models.CharField(verbose_name='国家/地区', max_length=128)
    movieID = models.IntegerField(verbose_name='电影ID', default=1111111)
    movieURL = models.CharField(verbose_name='URL', max_length=64, null=True)


class MovieDetails(models.Model):
    """ 电影详细信息表 """
    movieName = models.CharField(verbose_name='电影名', max_length=64)
    imageUrl = models.CharField(verbose_name='海报地址', max_length=128)
    movieScoring = models.DecimalField(verbose_name='评分', max_digits=3, decimal_places=1)
    commentNumber = models.IntegerField(verbose_name='评论人数')
    movieType = models.CharField(verbose_name='类型', max_length=64)
    releaseInfo = models.CharField(verbose_name='上映日期', max_length=128)
    duration = models.CharField(verbose_name='片长', max_length=64)
    director = models.CharField(verbose_name='导演', max_length=128)
    actors = models.TextField(verbose_name='主演')
    movieCountry = models.CharField(verbose_name='国家/地区', max_length=32)
    languages = models.CharField(verbose_name='语言', max_length=64)
    introduction = models.TextField(verbose_name='简介')


class MovieShortComment(models.Model):
    """ 电影短评情感分析表 """
    movieName = models.CharField(verbose_name='电影名', max_length=64)
    commentPerson = models.CharField(verbose_name='评论者', max_length=64)
    ratingScale = models.CharField(verbose_name='评分等级', max_length=16)
    commentDate = models.CharField(verbose_name='评论日期', max_length=32)
    starNumber = models.IntegerField(verbose_name='点赞数')
    emotionScored = models.CharField(verbose_name='情感得分', max_length=16, null=True)
    emotionScale = models.CharField(verbose_name='情感度', max_length=16, null=True)
    emotionTendency = models.CharField(verbose_name='情感倾向', max_length=8, null=True)
    commentHandle = models.TextField(verbose_name='处理后评论', null=True)
    commentContent = models.TextField(verbose_name='评论内容')


class FilmReview(models.Model):
    """ 电影影评表 """
    movieName = models.CharField(verbose_name='电影名', max_length=64)
    movieID = models.IntegerField(verbose_name='电影ID')
    userName = models.CharField(verbose_name='用户名', max_length=64)
    userID = models.IntegerField(verbose_name='用户ID')
    ratingScale = models.CharField(verbose_name='评分等级', max_length=16)
    commentDate = models.CharField(verbose_name='评论日期', max_length=32)
    usefulNumber = models.IntegerField(verbose_name='有用数')
    unusefulNumber = models.IntegerField(verbose_name='无用数')


class SimilarMovies(models.Model):
    """ 相似电影表 """
    movieName = models.CharField(verbose_name='电影名', max_length=64)
    similarMovies = models.TextField(verbose_name='相似电影列表')

