from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Mzalendo, Comment
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
        )
        widgets = {
            'username': forms.TextInput(attrs={
                
                'placeholder': 'Username'
            }),
            'password1': forms.PasswordInput(attrs={
                
                'placeholder': 'Password'
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Confirm Password'
            }),
        }

class MzalendoForm(forms.ModelForm):
    class Meta:
        model = Mzalendo
        fields = ['name', 'gender', 'age', 'cover', 'county', 'life']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 10,
                'cols': 40,
                'class': 'materialize-textarea'
                }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['post']
        widgets = {
                'comment': forms.Textarea(attrs={
                'rows': 10,
                'cols': 20,
                'class': 'materialize-textarea',
                'data-length': '500'
                }),
        }

    def clean_comment(self):
        data = self.cleaned_data['comment']
        if len(data) > 500:
            msg = 'Comment is too long. Please keep your comment under 500 characters.'
            self.add_error('comment', msg)
        if len(data) < 5:
            msg = 'Comment is too short.'
            self.add_error('comment', msg)
        return data