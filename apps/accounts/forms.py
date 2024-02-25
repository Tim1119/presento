from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm):

        model = User
        fields = ['email', 'full_name','password1','password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['email', 'full_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'





    