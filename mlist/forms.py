from django import forms
from review.models import Review, Comments

class DateInput(forms.DateInput):
    input_type = 'date'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']  
        labels = {
            'content': '내용',
        }

class Comment_form(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment_txt']
        labels = {
            'comment_txt': '댓글내용',
        }
