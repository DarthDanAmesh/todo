from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Mzalendo, Comment
from django import forms
from .models import Profile


class UpdateAccountProfile(UserCreationForm):
    model = User
    fields = ("username", "email")

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

    # regardless of CASE (lower,upper)
    def clean_username(self):
        username=self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('This username exists on system')
        return username

    # regardless of CASE (lower,upper)
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email exists on system')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.email = self.cleaned_data.get('email')
            user.is_active = False
            user.save()
        return user

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

class AccountProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user', 'avi')

class EditMzalendoForm(forms.ModelForm):
    class Meta:
        model = Mzalendo
        fields = ['name', 'gender', 'age', 'cover', 'county', 'life']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['life'].widget.attrs.update({'style': 'width: 250px;','background':'red;'})
        # add widgets if necessary

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