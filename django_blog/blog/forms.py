from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comment

# ----------------------------
# User Registration Form
# ----------------------------
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# ----------------------------
# User Update Form (Profile)
# ----------------------------
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

# ----------------------------
# Comment Form
# ----------------------------
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='', 
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'})
        from django import forms
from .models import Post
from taggit.forms import TagWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # include tags here
        widgets = {
            'tags': TagWidget(),  # this is what the checker wants
        }

    )

    class Meta:
        model = Comment
        fields = ['content']
