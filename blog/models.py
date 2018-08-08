from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError


# Model that describes a category


class Category(models.Model):
    category_name = models.CharField(max_length=32)
    slug = models.SlugField(unique=True, max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.category_name

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={"slug": self.slug})

    # Prevents new Categories from having the same name as existing categories.
    # This ensures unique slug url for categories
    def clean(self):
        temp = slugify(self.category_name)
        if Category.objects.filter(slug=temp).exists():
            category = Category.objects.get(slug=temp)
            if self.id is not category.id:
                name = slugify(category.category_name)
                if temp == name:
                    raise ValidationError('This category already exists.')

    # Entering categories is case insensitive for slug url, so 'General' is same as 'general'
    # This method only activates when your model updates go through save.
    # If you write code that does an .update() on a queryset, you will skip the slugify step
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

# Model that describes a blog post


class Post(models.Model):
    post_author = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    post_text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    post_title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return self.post_title

    def __str__(self):
        return self.post_title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={"slug": self.slug})

    def clean(self):
        temp = slugify(self.post_title)
        if Post.objects.filter(slug=temp).exists():
            post = Post.objects.get(slug=temp)
            if self.id is not post.id:
                title = slugify(post.post_title)
                if temp == title:
                    raise ValidationError('This post already exists.')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.post_title)
        super(Post, self).save(*args, **kwargs)
