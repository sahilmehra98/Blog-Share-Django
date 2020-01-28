from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def post_list(request):
    posts=Post.published.filter(author__email=request.user)
    return render(request, 'blog_post/list.html', {'posts':posts})

@login_required
def post_detail(request, year, month, day, slug):
    has_access=False
    raw_post=get_object_or_404(Post, slug=slug, status='published', publish__year=year, publish__month=month, publish__day=day)

    if raw_post.author == request.user:
        has_access=True
        post=raw_post
        return render(request, 'blog_post/detail.html', {'post':post, 'has_access':has_access})

    return render(request, 'blog_post/detail.html', {'has_access':has_access})
