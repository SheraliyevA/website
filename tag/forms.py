from django import forms
from .models import *


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'description',
            'tags',
			
        ]


class UserForm(forms.ModelForm):
	username=forms.CharField(label='',widget=forms.Textarea(
		attrs={
			'class':'form-control',
			'placeholder':'Username yozing...',
			'rows':2,
			'cols':50
		}
	))
	password=forms.CharField(label='',widget=forms.Textarea(
		attrs={
			'class':'form-control',
			'placeholder':'Password kiriting...',
			'rows':1,
			'cols':55
		}
	))
	email=forms.CharField(label='',widget=forms.Textarea(
		attrs={
			'class':'form-control',
			'placeholder':'Emailni kiriting',
			'rows':1,
			'cols':60,
		}
	))
	class Meta:
		model=User
		fields=['username','password','email']

	def save(self,commit=True):
		user=super().save(commit)
		user.set_password(self.cleaned_data['password'])
		user.save()
		return user 
        
class LoginForm(forms.Form):
	username=forms.CharField(label='',max_length=232,widget=forms.Textarea(
		attrs={
			'class':'form-control',
			'placeholder':'Username kiriting...',
			'rows':2,
			'cols':60
		}
	))
	password=forms.CharField(max_length=232)
    


	def __str__(self):
		return self.username

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
    
    # overriding default form setting and adding bootstrap class
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'placeholder': 'Enter name','class':'form-control'}
        self.fields['email'].widget.attrs = {'placeholder': 'Enter email', 'class':'form-control'}
        self.fields['body'].widget.attrs = {'placeholder': 'Comment here...', 'class':'form-control', 'rows':'5'}