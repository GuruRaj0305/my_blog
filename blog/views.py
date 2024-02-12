# from datetime import date
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView


# def get_date(post):
#     return post['date']


# Create your views here.

class StatingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]            #look at it 
    context_object_name = "posts"

    def get_queryset(self):
        query_Set = super().get_queryset()
        data = query_Set[:3]
        return data
    

class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"


class SinglePostView(DetailView):
    template_name = "blog/post-detail.html"
    model = Post   # here the dynamic path will autometically search with PK, if PK not matches then autometically with slug no need to change or add anything (this is also one of the feature of DetailedView)

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["post_tags"] = self.object.tags.all()
        return context



# below is function based view

# def index(request):
#     # sorted_posts = sorted(all_posts, key = get_date)
#     # latest_posts = sorted_posts[-3:]
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/index.html", {
#         "posts": latest_posts
#     })

# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     return render(request, "blog/all-posts.html",{
#         "all_posts": all_posts
#     })

# def post_detailed(request, slug):
#     # post_identifier = next(post for post in all_posts if post['slug']==slug)
#     # post_identifier = [post for post in all_posts if post['slug']==slug]
#     post_identifier = get_object_or_404(Post, slug = slug)
#     return render(request, "blog/post-detail.html", {
#         "post": post_identifier,
#         "post_tags": post_identifier.tags.all(),
#     })
