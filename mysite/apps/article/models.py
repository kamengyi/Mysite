import datetime
from django.db import models

class ArticleTag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=128)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        'login.User',               # 引用同项目不同应用的模型
        on_delete = models.CASCADE,   # models.CASCADE 该模型删除, 相应外键对应的模型也会被删除
        related_name = 'articles'
    )

    # 文章所属栏目
    column = models.ForeignKey(
        'ArticleColumn',
        null = True,
        blank = True,
        on_delete = models.CASCADE,
        related_name = 'articles'     # 反向引用, xxx.articles
    )

    # 文章标签, 和文章是多对多关系
    tags = models.ManyToManyField(
        ArticleTag,
        blank=True,
        related_name='articles'
    )
    
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title


class ArticleColumn(models.Model):
    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        verbose_name = '栏目'
        verbose_name_plural = '栏目'

    def __str__(self):
        return self.title

