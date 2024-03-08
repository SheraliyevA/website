from django.contrib import admin
from .models import *

class Admin(admin.ModelAdmin):
    list_display = ('title', 'published', 'post_author')
    prepopulated_fields = {"slug": ("title", )}

   

admin.site.register(Post,Admin)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('name', 'email', 'post', 'created', 'active')
    # if list_display in 'post':
    # return f"{self.post[:1]}"
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
# Register your models here.
