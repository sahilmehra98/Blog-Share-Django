from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

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
