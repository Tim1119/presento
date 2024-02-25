from django.urls import path
from .views import (ArticleHomeView, ArticleDetailView, ArticleUpdateView, ArticleCreateView,
                    ArticleDeleteView,ArticleDraftsListView, search_article,ArticleByCategory,
                    ArticleByTags,comment_create_view,like_or_unlike_article)

app_name = 'articles'

urlpatterns = [

    path('', ArticleHomeView.as_view(), name='home'),
    path('article/<str:slug>/', ArticleDetailView.as_view(), name='article-detail'),
    path('update-article/<str:slug>/', ArticleUpdateView.as_view(), name='update-article'),
    path('delete-article/<str:slug>/',ArticleDeleteView.as_view(), name='delete-article'),
    path('create-article/',ArticleCreateView.as_view(), name='create-article'),
    path('article-drafts/',ArticleDraftsListView.as_view(), name='draft-articles'),
    path('search-article/',search_article, name='search-article'),
    path('article-by-category/<str:category_slug>/',ArticleByCategory.as_view(), name='article-by-category'),
    path('article-by-tag/<str:tag_slug>/',ArticleByTags.as_view(), name='article-by-tag'),
    path('create-comment/<str:slug>/',comment_create_view, name='create-comment'),
    path('like_or_unlike_article/',like_or_unlike_article, name='like_or_unlike_article'),
]
