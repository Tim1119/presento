from django.forms import ModelForm
from .models import Profile


class ProfileForm(ModelForm):


    class Meta:
        model = Profile 
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


    

        