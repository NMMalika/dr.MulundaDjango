from django import forms
from .models import  Comment



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'phone_number', 'comment']
        
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Write your comment here...', 'rows': 4}),
        }
    

class ReplyForm(forms.Form):
    subject = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'vTextField'}), # Use admin styles
    )
    body = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'vLargeTextField', 'rows': 10}), # Use admin styles
    )