from django.shortcuts import render

from blog.models import Post


# Create your views here.

def blog(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'Блог',
    }
    return render(request, 'index/blog.html', context)


def blogPage(request, post_id):
    post = Post.objects.all().get(id=post_id)
    context = {
        'post': post,
        'title': f'{post.title}',
    }
    return render(request, 'index/news.html', context)