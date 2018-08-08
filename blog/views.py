from django.shortcuts import render
from django.views import generic
from .models import Post, Category
from taggit.models import Tag
from django.utils import timezone


# Generates context name for categories
class CategoryMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CategoryMixin, self).get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context


# Displays a list of posts by their categories
class CategoryIndexView(CategoryMixin, generic.ListView):
    template_name = "blog/history.html"
    model = Post
    paginate_by = 4
    context_object_name = 'latest_post_list'

    # Filters posts by category slug url and orders them by publication date
    def get_queryset(self):
        return Post.objects.filter(
            category__slug=self.kwargs.get('slug'),
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


# Generates context name for tags
class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


# Displays a list of posts by their tags
class TagIndexView(CategoryMixin, TagMixin, generic.ListView):
    template_name = "blog/history.html"
    model = Post
    paginate_by = 4
    context_object_name = 'latest_post_list'

    # Filters posts by tag slug url and orders them by publication date
    def get_queryset(self):
        return Post.objects.filter(
            tags__slug=self.kwargs.get('slug'),
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


# Displays a list of post
class PostList(CategoryMixin, TagMixin, generic.ListView):
    model = Post
    context_object_name = 'latest_post_list'
    paginate_by = 4

    # Return the last published posts (not including posts published in the future).
    def get_queryset(self):
        return Post.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


# Displays the content inside a post
class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'

    #  Excludes any posts that aren't published yet.
    def get_queryset(self):
        return Post.objects.filter(pub_date__lte=timezone.now())


# Displays the about page using the raw html file
def about_detail(request):
    return render(request, 'blog/about.html')


# Displays the portfolio page using the raw html file
def portfolio_detail(request):
    return render(request, 'blog/portfolio.html')
