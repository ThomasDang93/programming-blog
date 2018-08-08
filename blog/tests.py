import datetime
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db import models
from .models import Post, Category


def create_post_with_category(post_author, post_title, days, post_slug, category_name, category_slug):
    if Category.objects.filter(slug=category_name).exists():
        # if category already exists, just retrieve it
        category = Category.objects.get(slug=category_name)
        time = timezone.now() + datetime.timedelta(days=days)
        return Post.objects.create(post_author=post_author, post_title=post_title,
                                   pub_date=time, slug=post_slug, category=category)
    else:
        # if category does not exist, create a new one
        category = Category.objects.create(category_name=category_name, slug=category_slug)
        time = timezone.now() + datetime.timedelta(days=days)
        return Post.objects.create(post_author=post_author, post_title=post_title,
                                   pub_date=time, slug=post_slug, category=category)


def create_post(post_author, post_title, days, slug):
    """
    Create a post with the given `post_text` and published the
    given number of `days` offset to now (negative for post published
    in the past, positive for post that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Post.objects.create(post_author=post_author, post_title=post_title, pub_date=time, slug=slug)


class PostIndexViewTests(TestCase):

    def test_future_post(self):
        """
         Post with a pub_date in the future aren't displayed on
         the index page.
         """
        admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        title = "Future post."
        slug = models.SlugField(unique=True, max_length=200)
        slug = slugify(title)
        create_post(post_author=admin, post_title=title, days=30, slug=slug)
        response = self.client.get(reverse('blog:index'))
        self.assertContains(response, "No posts are available")
        self.assertQuerysetEqual(response.context['latest_post_list'], [])

    def test_no_post(self):
        """
        If no post exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts are available")
        self.assertQuerysetEqual(response.context['latest_post_list'], [])

    def test_past_post(self):
        """
        Posts with a pub_date in the past are displayed on the
        index page.
        """
        admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        title = "Past post."
        slug = models.SlugField(unique=True, max_length=200)
        slug = slugify(title)
        create_post(post_author=admin, post_title=title, days=-30, slug=slug)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Past post.>']
        )

    def test_future_and_past_post(self):
        """
        Even if both past and future posts exist, only past posts
        are displayed.
        """
        admin1 = User.objects.create_superuser('pastuser', 'myemail@test.com', 'password')
        admin2 = User.objects.create_superuser('futureuser', 'myemail@test.com', 'password')
        title1 = "Past post."
        title2 = "Future post."
        slug1 = models.SlugField(unique=True, max_length=200)
        slug2 = models.SlugField(unique=True, max_length=200)
        slug1 = slugify(title1)
        slug2 = slugify(title2)
        create_post(post_author=admin1, post_title=title1, days=-30, slug=slug1)
        create_post(post_author=admin2, post_title=title2, days=30, slug=slug2)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Past post.>']
        )

    def test_two_past_posts(self):
        # The post index page may display multiple post.
        admin1 = User.objects.create_superuser('pastuser1', 'myemail@test.com', 'password')
        admin2 = User.objects.create_superuser('pastuser2', 'myemail@test.com', 'password')
        title1 = "Past post 1."
        title2 = "Past post 2."
        slug1 = models.SlugField(unique=True, max_length=200)
        slug2 = models.SlugField(unique=True, max_length=200)
        slug1 = slugify(title1)
        slug2 = slugify(title2)
        create_post(post_author=admin1, post_title=title1, days=-30, slug=slug1)
        create_post(post_author=admin2, post_title=title2, days=-5, slug=slug2)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Past post 2.>', '<Post: Past post 1.>']
        )


class PostDetailViewTests(TestCase):

    def test_future_post(self):
        """
        The detail view of a post with a pub_date in the future
        returns a 404 not found.
        """
        admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        title = 'Future post.'
        slug = models.SlugField(unique=True, max_length=200)
        slug = slugify(title)
        future_post = create_post(post_author=admin, post_title=title, days=5, slug=slug)
        url = reverse('blog:detail', args=(future_post.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_post(self):
        """
        The detail view of a post with a pub_date in the past
        displays the post's text.
        """
        admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        title = 'Past post.'
        slug = models.SlugField(unique=True, max_length=200)
        slug = slugify(title)
        past_post = create_post(post_author=admin, post_title=title, days=-5, slug=slug)
        url = reverse('blog:detail', args=(past_post.slug,))
        response = self.client.get(url)
        self.assertContains(response, past_post.post_title)


class CateogryIndexViewTests(TestCase):
    def test_future_post_category(self):
        # Post with a pub_date in the future aren't displayed on
        # the category index page.
        admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        post_title = "Future post."
        post_slug = models.SlugField(unique=True, max_length=200)
        post_slug = slugify(post_title)
        category_name = "java"
        category_slug = models.SlugField(unique=True, max_length=100)
        category_slug = slugify(category_name)
        create_post_with_category(post_author=admin, post_title=post_title, days=30,
                                  post_slug=post_slug, category_name=category_name, category_slug=category_slug)
        response = self.client.get(reverse('blog:category', kwargs={"slug": category_slug}))
        self.assertContains(response, "No posts are available")
        self.assertQuerysetEqual(response.context['latest_post_list'], [])

    def test_no_post_category(self):
        # If no post exist in category index page, an appropriate message is displayed.
        category_name = "java"
        category_slug = models.SlugField(unique=True, max_length=100)
        category_slug = slugify(category_name)
        response = self.client.get(reverse('blog:category', kwargs={"slug": category_slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts are available")
        self.assertQuerysetEqual(response.context['latest_post_list'], [])

    def test_past_post_category(self):
        # Posts with a pub_date in the past are displayed on the
        # category index page.
        admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        post_title = "Past post."
        post_slug = models.SlugField(unique=True, max_length=200)
        post_slug = slugify(post_title)
        category_name = "java"
        category_slug = models.SlugField(unique=True, max_length=100)
        category_slug = slugify(category_name)
        create_post_with_category(post_author=admin, post_title=post_title, days=-30,
                                  post_slug=post_slug, category_name=category_name, category_slug=category_slug)
        response = self.client.get(reverse('blog:category', kwargs={"slug": category_slug}))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Past post.>']
        )

    def test_future_past_post_category(self):
        # Even if both past and future posts exist, only past posts
        # are displayed in category index.
        admin = User.objects.create_superuser('pastuser', 'myemail@test.com', 'password')
        post_title = "Past post."
        post_slug = models.SlugField(unique=True, max_length=200)
        post_slug = slugify(post_title)

        admin2 = User.objects.create_superuser('futureuser', 'myemail@test.com', 'password')
        post_title2 = "Future post."
        post_slug2 = models.SlugField(unique=True, max_length=100)
        post_slug2 = slugify(post_title2)

        category_name = "java"
        category_slug = models.SlugField(unique=True, max_length=100)
        category_slug = slugify(category_name)

        create_post_with_category(post_author=admin, post_title=post_title, days=-30,
                                  post_slug=post_slug, category_name=category_name, category_slug=category_slug)
        create_post_with_category(post_author=admin2, post_title=post_title2, days=30,
                                  post_slug=post_slug2, category_name=category_name, category_slug=category_slug)
        response = self.client.get(reverse('blog:category', kwargs={"slug": category_slug}))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Past post.>']
        )

    def test_two_past_post_category(self):
        # The category post index page may display multiple past posts.
        admin = User.objects.create_superuser('pastuser1', 'myemail@test.com', 'password')
        post_title = "Past post 1."
        post_slug = models.SlugField(unique=True, max_length=200)
        post_slug = slugify(post_title)

        admin2 = User.objects.create_superuser('pastuser2', 'myemail@test.com', 'password')
        post_title2 = "Past post 2."
        post_slug2 = models.SlugField(unique=True, max_length=100)
        post_slug2 = slugify(post_title2)

        category_name = "java"
        category_slug = models.SlugField(unique=True, max_length=100)
        category_slug = slugify(category_name)

        create_post_with_category(post_author=admin, post_title=post_title, days=-30,
                                  post_slug=post_slug, category_name=category_name, category_slug=category_slug)
        create_post_with_category(post_author=admin2, post_title=post_title2, days=-5,
                                  post_slug=post_slug2, category_name=category_name, category_slug=category_slug)
        response = self.client.get(reverse('blog:category', kwargs={"slug": category_slug}))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Past post 2.>', '<Post: Past post 1.>']
        )
