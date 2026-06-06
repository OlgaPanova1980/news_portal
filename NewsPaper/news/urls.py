from django.urls import path
from .views import (
    NewsList, NewsDetail, PostSearch,
    NewsCreate, NewsEdit, NewsDelete,
    ArticleCreate, ArticleEdit, ArticleDelete
)

urlpatterns = [
    path('', NewsList.as_view(), name='product_list'),
    path('<int:pk>', NewsDetail.as_view(), name='product_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),

    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]