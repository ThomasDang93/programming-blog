from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostList.as_view(template_name="blog/index.html"), name='index'),
    path('portfolio/', views.portfolio_detail, name='portfolio'),
    path('history/', views.PostList.as_view(template_name="blog/history.html"), name='history'),
    path('post/<slug:slug>/', views.PostDetail.as_view(), name='detail'),
    path('about/', views.about_detail, name='about'),
    path('tag/<slug:slug>/', views.TagIndexView.as_view(), name='tagged'),
    path('category/<slug:slug>/', views.CategoryIndexView.as_view(), name='category'),
]
