from django.contrib import admin
from .models import Comment, Post, Subscribe

admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Subscribe)
