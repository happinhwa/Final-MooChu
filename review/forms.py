from django import forms
from .models import Review, Comments

class DateInput(forms.DateInput):
    input_type = 'date'

class ReviewForm(forms.ModelForm):
    review = forms.CharField(label='간단히 기록하기:', widget=forms.Textarea(attrs={'cols': '40', 'rows': '5'}))

    class Meta:
        model = Review
        fields = ['review']

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment_txt']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["comment_txt"].label = "댓글"
        self.fields["comment_txt"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "댓글을 입력하세요."
        })

