from django.urls import path, re_path
from . import views

app_name = 'blog'

urlpatterns = [
    path('detail/<str:slug>', views.blog_post_detail_view, name="blog_post_detail_page"),
    path('', views.blog_post_list_view, name="blog_post_list_view"),
    path('create', views.blog_post_create_view, name="blog_post_create_view"),
    path('update/<str:slug>', views.blog_post_update_view, name="blog_post_update_view"),
    path('delete/<str:slug>', views.blog_post_delete_view, name="blog_post_delete_view"),
    #re_path(r'(?P<slug>\w+)$', views.blog_post_detail_page, name="blog_post_detail_page"),
    #127.0.0.1/blog/
]