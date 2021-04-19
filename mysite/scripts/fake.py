# -*- coding:utf-8 -*-

import os
import pathlib
import random
import sys
from datetime import timedelta

import django
import faker
from django.utils import timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    django.setup()

    from apps.article.models import Article, ArticleColumn, ArticleTag
    from apps.login.models import User

    column_list = ['测试', 'HTML', 'CSS', 'JavaScript', 'Python', 'Java']
    tag_list = ['测试', 'HTML', 'CSS', 'JavaScript', 'Python', 'Java']

    print('创建标签')
    for tag in tag_list:
        if ArticleTag.objects.get(name=tag):
            pass
        else:
            ArticleTag.objects.create(name=tag)

    print('创建栏目')
    for name in column_list:
        if ArticleColumn.objects.get(title=name):
            pass
        else:
            ArticleColumn.objects.create(title=name)

    print('创建文章')
    fake = faker.Faker('zh_CN')
    for _ in range(100):
        tags = ArticleTag.objects.order_by('?')
        tag1 = tags.first()
        tag2 = tags.last()
        column = ArticleColumn.objects.order_by('?').first()
        user = User.objects.order_by('?').first()
        article = Article.objects.create(
            title = fake.sentence().rstrip(),
            body = ''.join(fake.paragraphs(10)),
            user = user,
            column = column,
        )

        article.tags.add(tag1, tag2)
        article.save()

    print('完成')

