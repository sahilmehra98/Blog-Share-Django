from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
@login_required
def post_list(request):
    object_list=Post.published.filter(author__email=request.user)
    #3 posts per page
    paginator=Paginator(object_list, 3)
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        #If page is not an integer, deliver the first page
        posts=paginator.page(1)
    except EmptyPage:
        #if page is out of range, deliver last page of results
        posts=paginator.page(paginator.num_pages)

    return render(request, 'blog_post/list.html', {'posts':posts, 'page':page})

@login_required
def post_detail(request, year, month, day, slug):
    has_access=False
    raw_post=get_object_or_404(Post, slug=slug, status='published', publish__year=year, publish__month=month, publish__day=day)

    if raw_post.author == request.user:
        has_access=True
        post=raw_post
        return render(request, 'blog_post/detail.html', {'post':post, 'has_access':has_access})

    return render(request, 'blog_post/detail.html', {'has_access':has_access})
