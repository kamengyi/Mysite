import markdown
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from apps.login.models import User
from .models import ArticleColumn, Article
from django.core.paginator import Paginator

# Create your views here.

# 检测是否登录, 登录完成即可进行其他操作
def check_required(func):
    def inner(*args, **kwargs):
        if not request.session.get('is_login', None):
            return HttpResponseRedirect(reverse('index'))
    return inner


def article_create(request):
    if request.method == 'POST':
        article_form = ArticleForm(data=request.POST)
        if article_form.is_valid():
            new_article = article_form.save(commit=False)
            try:
                user = User.objects.get(username=request.session.get('user_name', None))
            except User.DoesNotExist:
                message = "用户不存在"
                return render(request, 'article/create.html', locals())

            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])

            message = "成功新建文章"
            new_article.user = user
            new_article.save()
            # 以下是防止刷新浏览器出现重复提交数据的现象
            # return HttpResponseRedirect(reverse('index')), 下面方法也能起到相同效果
            return redirect(reverse('index'))
        else:
            print(article_form.errors)
            message = "请检查内容"
            return render(request, 'article/create.html', locals())
    else:
        columns = ArticleColumn.objects.all()
        return render(request, 'article/create.html', locals())


def article_list(request):
    try:
        article_list = Article.objects.all()
    except:
        article_list = []
    
    # 每页展示10篇文章
    p = Paginator(article_list, 10)
    # 获取请求页码
    page = request.GET.get('page')
    # p.get_page() -> 返回页码内容
    articles = p.get_page(page)

    context = {'articles': articles}
    return render(request, 'article/list.html', context)


def article_update(request):
    pass


def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    article.body = markdown.markdown(article.body,
        extensions = [
            # 基础扩展
            'markdown.extensions.extra',
            # 代码高亮
            'markdown.extensions.codehilite',
            # toc目录生成
            'markdown.extensions.toc',
    ])

    context = {'article': article}
    return render(request, 'article/detail.html', context)

