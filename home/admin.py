from django.contrib import admin

from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'datetime_modified', 'datetime_created',]
    search_fields = ['slug',]
    list_filter = ['datetime_modified',]
    prepopulated_fields = {'slug':('title',),}
    raw_id_fields = ['user',]
