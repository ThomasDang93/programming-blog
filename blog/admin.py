from django.contrib import admin
from .models import Post, Category
from django.db import models
from martor.widgets import AdminMartorWidget
# Link that redirects to main website
admin.site.site_url = 'https://www.putyourwebsitehere2345.com'

# Admin section to manage posts


class PostAdmin(admin.ModelAdmin):
    # Markdown editor integration
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    # Form for the user to make a post
    fieldsets = [
        (None, {'fields': ['post_author']}),
        (None, {'fields': ['post_title']}),
        (None, {'fields': ['post_text']}),
        (None, {'fields': ['category']}),
        (None, {'fields': ['tags']}),
        ('Published Date', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]

    list_display = ('post_author', 'post_title', 'category', 'pub_date')
    list_filter = ['pub_date', 'category', 'tags']
    search_fields = ['post_title']


# Admin section to manage categories


class CategoryAdmin(admin.ModelAdmin):

    # Form for the user to make a category
    fieldsets = [
        (None, {'fields': ['category_name']}),
    ]

    list_display = ('category_name',)
    search_fields = ['category_name']


# Register the custom admins


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
