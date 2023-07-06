from django import forms
from django.contrib.auth.forms import UserCreationForm
<<<<<<< HEAD
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Genre
=======
from django.contrib.auth.models import User
from .models import User, GuestNote
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
>>>>>>> 83a6f906ce52793cf023ad350d400459f3115126

User = get_user_model()

class RegistrationForm(UserCreationForm):
    username = forms.CharField(label="아이디", max_length=20, help_text='사용할 아이디를 입력해주세요.')
    email = forms.EmailField(max_length=50, help_text='이메일을 입력해주세요.')
    nickname = forms.CharField(label="닉네임", max_length=20, help_text='닉네임을 입력해주세요.')
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput, help_text='비밀번호를 입력해주세요.')
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput, help_text='비밀번호를 한 번 더 입력해주세요.')
    birth = forms.DateField(label='생년월일', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    gender = forms.ChoiceField(label='성별', choices=(('male', '남성'), ('female', '여성')), required=False)

    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('이미 사용 중인 이메일입니다.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('이미 사용 중인 아이디입니다.')
        return username
    
    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if User.objects.filter(nickname=nickname).exists():
            raise ValidationError('이미 사용 중인 닉네임입니다.')
        return nickname
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.is_active=False
            user.save()
        return user

    class Meta:
        model = User
<<<<<<< HEAD
        fields = ['username', 'password1', 'password2', 'nickname', 'birth', 'gender', 'email']

class GenreSelectForm(forms.Form):
    selected_genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
=======
        fields = ['username', 'password1', 'password2', 'nickname', 'birth', 'gender','email']

class GuestNoteForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), max_length=500)


class ProfileUpdateForm(forms.ModelForm):
    nickname = forms.CharField(max_length=50, required=False)
    fav_genre = forms.CharField(max_length=100, required=False)
    profile_img = forms.ImageField(required=False)
    comment = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['nickname', 'fav_genre', 'profile_img', 'comment']
>>>>>>> 83a6f906ce52793cf023ad350d400459f3115126
