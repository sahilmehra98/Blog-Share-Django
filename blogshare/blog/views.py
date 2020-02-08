from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .forms import AddPostForm, EditPostForm

from rest_framework import generics
from .serializers import PostSerializer
from rest_framework.authentication import TokenAuthentication
from .permissions import EditOwnPost
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class PostListView(ListView):
    context_object_name='posts'
    paginate_by=3
    template_name='blog/post/list.html'

    def get_queryset(self):
        return Post.published.filter(author__email=self.request.user)

@login_required
def post_detail(request, year, month, day, slug):
    has_access=False
    raw_post=get_object_or_404(Post, slug=slug, status='published', publish__year=year, publish__month=month, publish__day=day)

    if raw_post.author == request.user:
        has_access=True
        post=raw_post
        return render(request, 'blog/post/detail.html', {'post':post, 'has_access':has_access})

    return render(request, 'blog/post/detail.html', {'has_access':has_access})

@login_required
def addPost(request):
    if request.method=='POST':
        form=AddPostForm(request.POST)
        if form.is_valid():
            #create a new post object but dont save yet
            new_post=form.save(commit=False)
            #Add author
            new_post.author=request.user
            #now save
            new_post.save()
            #redirect to blog/
            return redirect('../')
    else:
        form=AddPostForm()
    return render(request, 'blog/post/add_post.html', {'form':form})

@login_required
def edit(request, year, month, day, slug):
    has_access=False
    raw_post=get_object_or_404(Post, slug=slug, status='published', publish__year=year, publish__month=month, publish__day=day)
    if raw_post.author == request.user:
        has_access=True
    else:
        return render(request, 'blog/post/edit.html', {'has_access':has_access})
    if request.method=='POST':
        edit_form=EditPostForm(instance=raw_post, data=request.POST)
        if edit_form.is_valid():
            edit_form.save()
    else:
        edit_form=EditPostForm(instance=raw_post)
    return render(request, 'blog/post/edit.html', {'edit_form': edit_form, 'has_access':has_access})


#API views

class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.published.filter(author__email=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetail(generics.RetrieveUpdateAPIView):
    serializer_class = PostSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes = [EditOwnPost, IsAuthenticated]

    def get_queryset(self):
        return Post.published.filter(author__email=self.request.user)
