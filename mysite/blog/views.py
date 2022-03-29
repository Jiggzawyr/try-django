from math import log

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.utils import timezone

# Create your views here.
from .models import BlogPost
from .forms import BlogPostModelForm

def blog_post_list_view(request):
    now = timezone.now()
    qs = BlogPost.objects.all().published()
    #qs = BlogPost.objects.filter(publish_date__lte=now)
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        qs = (  qs | my_qs).distinct()
    template_name = 'blog/list.html'
    context = {"object_list": qs}
    return render(request, template_name, context)

#@login_required
@staff_member_required
def blog_post_create_view(request):
    form = BlogPostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.title = form.cleaned_data.get("title")
        obj.save()
        form = BlogPostModelForm()
    template_name = 'blog/form.html'
    context = {"form": form, "action" : "./create"}
    return render(request, template_name, context)

def blog_post_detail_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'blog/detail.html'
    context = {"object": obj}
    return render(request, template_name, context)

@staff_member_required
def blog_post_update_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    template_name = 'blog/form.html'
    context = {"title": f"Update {obj.title}", "action" : "./"+slug, "form": form }
    return render(request, template_name, context)

@staff_member_required
def blog_post_delete_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'blog/delete.html'
    if request.method == "POST":
        obj.delete()
        return redirect("/blog")
    context = {"object": obj}
    return render(request, template_name, context)