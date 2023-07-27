# forms.py
from django import forms
from .models import Review, Comments

class DateInput(forms.DateInput):
    input_type = 'date'

class ReviewForm(forms.ModelForm):
    writer = forms.CharField(widget=forms.HiddenInput(), required=False)
    movie_title = forms.CharField(widget=forms.HiddenInput(), required=False)  # Add the movie_title field

    class Meta:
        model = Review
        fields = ['content', 'rating', 'writer', 'movie_title']  # Add 'movie_title' field to the form
        labels = {
            'content': '내용',
            'rating': '평점',
            'writer': '작성자',
            'movie_title': '영화 제목',  # Set the label for the movie_title field
        }


        
class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment_txt']
        labels = {
            'comment_txt': '댓글내용',
        }
