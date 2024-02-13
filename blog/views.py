# from datetime import date
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView
from .forms import CommentForm
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

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


# class SinglePostView(DetailView):
#     template_name = "blog/post-detail.html"
#     model = Post   # here the dynamic path will autometically search with PK, if PK not matches then autometically with slug no need to change or add anything (this is also one of the feature of DetailedView)

#     def get_context_data(self, **kwargs: Any):
#         context = super().get_context_data(**kwargs)
#         context["post_tags"] = self.object.tags.all()
#         context["comment_form"] = CommentForm()
#         return context


class SinglePostView(View):
        def is_save_later(self, request, post_id):
            stored_post = request.session.get("stored_post")
            if stored_post is not None:
                is_save_for_later = post_id in stored_post
            else:
                is_save_for_later = False

            return is_save_for_later

        def get(self, request, slug):
            post= Post.objects.get(slug = slug)
            
            context = {
                 "post": post,
                 "post_tags": post.tags.all(),
                 "comment_form": CommentForm(),
                 "comments": post.comments.all().order_by("-id"),
                 "is_saved_for_later": self.is_save_later(request, post.id)
            }
            return render(request, "blog/post-detail.html", context)
        


        def post(self, request, slug):
            comment_form = CommentForm(request.POST)
            post= Post.objects.get(slug = slug)
            
            if comment_form.is_valid():
                 comment = comment_form.save(commit=False)
                 comment.post = post
                 comment.save()
                 return HttpResponseRedirect(reverse("posts-detailed-page", args=[slug]))
            context = {
                 "post": post,
                 "post_tags": post.tags.all(),
                 "comment_form": comment_form,
                 "comments": post.comments.all().order_by("-id"),
                 "is_saved_for_later": self.is_save_later(request, post.id)
            }
            return render(request, "blog/post-detail.html", context)
        

class ReadLaterView(View):
     def get(self, request):
         stored_post = request.session.get("stored_post")
         context = {}
         if stored_post is None or len(stored_post) == 0:
             context["post"] = []
             context["has_posts"] = False
         else:
             posts = Post.objects.filter(id__in = stored_post)
             context["posts"] = posts
             context["has_posts"] = True

         return render(request, "blog/stored-post.html", context)

     def post(self,request):
        stored_post = request.session.get("stored_post")

        if stored_post is None:
            stored_post = []
        
        post_id = int(request.POST["post_id"])

        if post_id not in stored_post:            
            stored_post.append(post_id)
        else:
            stored_post.remove(post_id)
        request.session["stored_post"] = stored_post
        
        return HttpResponseRedirect("/")
            
            
        
          


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
