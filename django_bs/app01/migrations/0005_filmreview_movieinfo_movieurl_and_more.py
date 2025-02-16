# Generated by Django 5.1 on 2024-09-03 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_movieinfo_movieid_alter_movieinfo_releaseinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilmReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movieName', models.CharField(max_length=64, verbose_name='电影名')),
                ('movieID', models.IntegerField(verbose_name='电影ID')),
                ('userName', models.CharField(max_length=64, verbose_name='用户名')),
                ('userID', models.IntegerField(verbose_name='用户ID')),
                ('ratingScale', models.CharField(max_length=16, verbose_name='评分等级')),
                ('commentDate', models.CharField(max_length=32, verbose_name='评论日期')),
                ('usefulNumber', models.IntegerField(verbose_name='有用数')),
                ('unusefulNumber', models.IntegerField(verbose_name='无用数')),
            ],
        ),
        migrations.AddField(
            model_name='movieinfo',
            name='movieURL',
            field=models.CharField(max_length=64, null=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='movieinfo',
            name='releaseInfo',
            field=models.CharField(max_length=64, verbose_name='上映日期'),
        ),
    ]
