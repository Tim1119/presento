from .models import Category,Tags

def categories(request):
    return {'article_categories': Category.objects.all()}

def tags(request):
    return {'article_tags': Tags.objects.all()}
