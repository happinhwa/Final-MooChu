from django import forms
from review.models import Review, Comments

class DateInput(forms.DateInput):
    input_type = 'date'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'rating']  # Include 'rating' field in the form
        labels = {
            'title': '제목',
            'content': '내용',
            'rating': '평점',
        }

class Comment_form(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment_txt']
        labels = {
            'comment_txt': '댓글내용',
        }
