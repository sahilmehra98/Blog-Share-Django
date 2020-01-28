from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .forms import AddPostForm

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

            return redirect('../')
            #return redirect(post_detail, year=new_post.publish.year, month=new_post.publish.month, day=new_post.publish.day, slug=new_post.slug)
    else:
        form=AddPostForm()
    return render(request, 'blog/post/add_post.html', {'form':form})
