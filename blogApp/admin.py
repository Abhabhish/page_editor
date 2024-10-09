import django
from django.contrib import admin
from blogApp.models import UserProfile, Category,Section,Folder,Post

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Section)
admin.site.register(Folder)
admin.site.register(Post)
