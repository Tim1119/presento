from .models import Article
from django.forms import ModelForm
from django_quill.forms import QuillFormField
from .models import Comment


class ArticleForm(ModelForm):
    error_class = 'error'

    class Meta:
        model = Article
        # content = QuillFormField() 
        exclude = ['author', 'approved', 'likes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'