from . import views
from django.urls import path

app_name = 'article'

urlpatterns = [
    path('article-create/', views.article_create, name='article_create'),
    path('article-update/', views.article_update, name='article_update'),
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),
    path('article-list/', views.article_list, name='article_list'),
]

