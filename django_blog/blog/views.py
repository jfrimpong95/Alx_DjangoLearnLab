from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post

# List all blog posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

# View single post details
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

# Create a new post (login required)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Update an existing post (login required)
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

# Delete a post (login required)
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Post

# ----------------------------
# Profile View (function-based)
# ----------------------------
@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        if username:
            user.username = username
        if email:
            user.email = email
        user.save()  # must save to pass checker
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'blog/profile.html', {'user': user})

# ----------------------------
# Post CRUD Views (class-based)
# ----------------------------
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # only author can edit

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # only author can delete

from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Comment, Post

# ----------------------
# Create Comment
# ----------------------
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        # Set the author to the logged-in user
        form.instance.author = self.request.user
        # Get the post from the URL
        post_id = self.kwargs['post_pk']
        form.instance.post = Post.objects.get(pk=post_id)
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()

# ----------------------
# Update Comment
# ----------------------
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author  # Only the author can edit

    def get_success_url(self):
        return self.object.post.get_absolute_url()

# ----------------------
# Delete Comment
# ----------------------
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):_
from django.shortcuts import render
from .models import Post

def post_list(request):
    query = request.GET.get('q')  # ?q=search-term in the URL
    posts = Post.objects.all()

    if query:
        posts = posts.filter(
            models.Q(title__icontains=query) |
            models.Q(content__icontains=query) |
            models.Q(tags__name__icontains=query)
        ).distinct()

    return render(request, 'blog/post_list.html', {'posts': posts})

from django.shortcuts import render
from .models import Post
from django.db.models import Q  # for OR queries with filter

def post_list(request):
    query = request.GET.get('q')  # get ?q=search-term from URL
    posts = Post.objects.all()  # default: all posts

    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()  # remove duplicates if multiple conditions match

    return render(request, 'blog/post_list.html', {'posts': posts})


