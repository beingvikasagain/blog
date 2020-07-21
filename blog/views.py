from django.shortcuts import render, get_object_or_404, redirect
from . forms import CommentForm,PostForm

from django.utils import timezone
from . models import Comment,Post

from django.views import generic
from django.urls import reverse, reverse_lazy

from django.contrib.auth import login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Create your views here.

def user_logout(request):
    logout(request)
    return redirect('blog:post_list')

class PostListView(generic.ListView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(generic.DetailView):
    model = Post

class PostCreateView(generic.CreateView,LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post
    form_class = PostForm

class PostUpdateView(generic.UpdateView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    model = Post
    fields = ('title','text')

class PostDeleteView(generic.DeleteView, LoginRequiredMixin):
    login_url = '/login/'
    model = Post
    success_url = reverse_lazy('blog:post_list')

class DraftList(generic.ListView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name='blog/post_list.html'
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_draft_list.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail', pk=post.pk)

@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method=='POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.approve()
    return redirect('blog:post_detail',pk=post_pk)

@login_required
def comment_delete(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:post_detail',pk=post_pk)
