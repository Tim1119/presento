from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Article, Category, Tags
from .forms import ArticleForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
# from apps.comments.forms import CommentForm
from django.views.decorators.http import require_http_methods
from apps.profiles.models import Profile
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from .models import Comment
from .forms import CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.


class ArticleHomeView(LoginRequiredMixin,ListView):
    model = Article
    template_name = "articles/home.html"
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(status='Published', approved=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.annotate(num_published_articles=Count('article', filter=Q(article__status=Article.ArticleStatus.Published)))
        recent_articles = Article.objects.all().filter(status='Published',)[::5]
        tags = Tags.objects.all()
        context['categories'] = categories
        context['recent_articles'] = recent_articles
        context['tags'] = tags
        return context


class ArticleDetailView(LoginRequiredMixin,DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'articles/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        categories = Category.objects.annotate(num_published_articles=Count('article', filter=Q(article__status=Article.ArticleStatus.Published)))
        recent_articles = Article.objects.all().exclude(
            slug=self.kwargs['slug'])[::5]
        tags = Tags.objects.all()
        context['categories'] = categories
        context['recent_articles'] = recent_articles
        context['tags'] = tags
        context['form'] = form
        return context


class ArticleCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('articles:home')
    success_message = 'Article has been created succesfully'
    template_name = 'articles/create_article.html'

    def get_form_kwargs(self):
        kwargs = super(ArticleCreateView, self).get_form_kwargs()
        if kwargs['instance'] is None:
            kwargs['instance'] = Article()
        kwargs['instance'].author = self.request.user.profile
        return kwargs


class ArticleUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/update_article.html"
    success_message = "Article was updated successfully"
    success_url = reverse_lazy('articles:home')

    def get_object(self, queryset=None):
        obj = super(ArticleUpdateView, self).get_object()
        if not obj.author.user == self.request.user:
            raise PermissionDenied("You don't have permission to update an article you didn't create")
        return obj


class ArticleDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Article
    success_message = "Article was deleted successfully"
    success_url = reverse_lazy('articles:home')

    def get_object(self, queryset=None):
        obj = super(ArticleDeleteView, self).get_object()
        if not obj.author.user == self.request.user:
            raise PermissionDenied(
                "You don't have permission to delete an article you didn't create")
        return obj

class ArticleByCategory(LoginRequiredMixin,ListView):
    model = Category
    template_name = "articles/article_by_category.html"
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        category = Category.objects.get(slug=category_slug)
        qs = Article.objects.filter(category=category, status='Published', approved=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.annotate(num_published_articles=Count('article', filter=Q(article__status=Article.ArticleStatus.Published)))
        recent_articles = Article.objects.all().filter(status='Published',)[::5]
        tags = Tags.objects.all()
        context['categories'] = categories
        context['recent_articles'] = recent_articles
        context['tags'] = tags
        context['searched_category'] = self.kwargs.get('category_slug')
        return context

class ArticleByTags(LoginRequiredMixin,ListView):
    model = Tags
    template_name = "articles/article_by_tag.html"
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        tag = Tags.objects.get(slug=tag_slug)
        qs = Article.objects.filter(tag=tag, status='Published', approved=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.annotate(num_published_articles=Count('article', filter=Q(article__status=Article.ArticleStatus.Published)))
        recent_articles = Article.objects.all().filter(status='Published',)[::5]
        tags = Tags.objects.all()
        context['categories'] = categories
        context['recent_articles'] = recent_articles
        context['tags'] = tags
        context['searched_tags'] = self.kwargs.get('tag_slug')
        return context

@login_required()
@require_http_methods('POST')
def comment_create_view(request,slug):
    current_user_profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            article = get_object_or_404(Article, slug=slug)
            instance = form.save(commit=False)
            instance.author = current_user_profile
            instance.article = article
            form.save()
            messages.success(request, 'comment has been created succesfully')
            return redirect('articles:article-detail', slug=slug)
        else:
            messages.error(request,'comment can not be created due to an error')
            return redirect('articles:article-detail', slug=slug)

@login_required()
@require_http_methods('GET')
def search_article(request):
    if request.method == "GET":
        search_query = request.GET.get('search_query')
        categories = Category.objects.annotate(num_published_articles=Count('article', filter=Q(article__status=Article.ArticleStatus.Published)))
        recent_articles = Article.objects.all().filter(status='Published',)[::5]
        tags = Tags.objects.all()
        articles = Article.objects.filter(title__icontains=search_query)
        return render(request, 'articles/searched_article.html', {'articles': articles, 'categories': categories, "recent_articles": recent_articles, 'tags': tags, 'searched_query': search_query})

@login_required()
@require_http_methods('POST')
def like_or_unlike_article(request):
    article_slug = request.POST.get('article_slug')
    article = get_object_or_404(Article, slug=article_slug)
    user_profile = request.user.profile  # Assuming user is authenticated
    if request.method == 'POST':
        # If the request is a POST request, toggle the like status
        article.toggle_like(user_profile)
        # Redirect back to the same page to update the like status
        return redirect('articles:article-detail', slug=article_slug)
    else:
        messages.error(request,'you could not like the article due to an error')
        return redirect('articles:article-detail', slug=article_slug)

class ArticleDraftsListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "articles/draft_articles.html"
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        profile = get_object_or_404(Profile, user=self.request.user)
        return qs.filter(status='Draft', author=profile, approved=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.annotate(num_published_articles=Count('article', filter=Q(article__status=Article.ArticleStatus.Published)))
        recent_articles = Article.objects.all().filter(status='Published',)[::5]
        tags = Tags.objects.all()
        context['categories'] = categories
        context['recent_articles'] = recent_articles
        context['tags'] = tags
        return context
