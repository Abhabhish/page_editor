from unicodedata import category
from django.db import models
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    contact = models.CharField(max_length=250)
    dob = models.DateField(blank=True, null = True)
    address = models.TextField(blank=True, null = True)
    avatar = models.ImageField(blank=True, null = True, upload_to= 'images/')
    user_type = models.IntegerField(default = 2)


    def __str__(self):
        return self.user.username
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print(instance)
    try:
        profile = UserProfile.objects.get(user = instance)
    except Exception as e:
        UserProfile.objects.create(user=instance)
    instance.profile.save()

class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    status = models.IntegerField(default = 1)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Section(models.Model):
    title = models.CharField(max_length=200)
    theme = models.ImageField(blank=True, null = True, upload_to= 'images/')
    def __str__(self):
        return self.title

class Folder(models.Model):
    section = models.ForeignKey(Section,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    parent_folder = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subfolders')

    def __str__(self):
        return self.name

class SeoAttributesList(models.Model):
    meta_name_description = models.CharField(max_length=1000,null=True,blank=True)
    meta_name_keywords = models.CharField(max_length=1000,null=True,blank=True)
    meta_property_og_title = models.CharField(max_length=1000,null=True,blank=True)
    meta_property_og_url = models.CharField(max_length=1000,null=True,blank=True)
    meta_property_og_description = models.CharField(max_length=1000,null=True,blank=True)
    meta_property_og_image = models.CharField(max_length=1000,null=True,blank=True)
    meta_name_twitter_card = models.CharField(max_length=1000,null=True,blank=True)
    meta_name_twitter_site = models.CharField(max_length=1000,null=True,blank=True)
    meta_name_twitter_title = models.CharField(max_length=1000,null=True,blank=True)
    meta_name_twitter_description = models.CharField(max_length=1000,null=True,blank=True)
    meta_name_twitter_image_src = models.CharField(max_length=1000,null=True,blank=True)
    meta_name_viewport = models.CharField(max_length=1000,null=True,blank=True)
    canonical = models.CharField(max_length=200)

    def __str__(self):
        return f"SEO Attributes for {self.post.page_name}"


class Post(models.Model):
    folder = models.ForeignKey('Folder', null=True, blank=True, on_delete=models.CASCADE, related_name='posts')
    page_name = models.CharField(max_length=100,null=True)
    page_title = models.CharField(max_length=125,null=True)
    side_panel = models.TextField(null=True)
    map_image = models.TextField(null=True)
    body_content = models.TextField(null=True)
    static_table = models.TextField(null=True)
    dynamic_table = models.TextField(null=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    seo_attributes = models.OneToOneField(SeoAttributesList,null=True,blank=True,on_delete=models.CASCADE,related_name='post')

    def generate_slug(self):
        slug_parts = [self.page_name]
        current_folder = self.folder
        while current_folder:
            slug_parts.insert(0, current_folder.name)
            current_folder = current_folder.parent_folder        
        return '/'.join(slug_parts)

    def save(self, *args, **kwargs):
        self.slug = self.generate_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.page_name


class OtherMaps(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images',null=True)
    map_name = models.CharField(max_length=200)
    thumbnail = models.ImageField()
    alt = models.CharField(max_length=200)
    redirection_url = models.CharField(max_length=255, null=True, blank=True)

    def generate_redirection_url(self):
        slug = self.post.slug
        slug_parts = slug.split('/')
        slug_parts.pop()
        slug_parts.append(slef.map_name)
        return '/'.join(slug_parts)

    def save(self, *args, **kwargs):
        self.redirection_url = self.generate_redirection_url()
        super().save(*args, **kwargs)


class PageHindi(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    title = models.TextField()
    blog_post = models.TextField()
    banner = models.ImageField(blank=True, null = True, upload_to= 'images/') 
    def __str__(self):
        return self.title

class PageBengali(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    title = models.TextField()
    blog_post = models.TextField()
    banner = models.ImageField(blank=True, null = True, upload_to= 'images/')
    def __str__(self):
        return self.title

class PageTamil(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    title = models.TextField()
    blog_post = models.TextField()
    banner = models.ImageField(blank=True, null = True, upload_to= 'images/')
    def __str__(self):
        return self.title

class PageMarathi(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    title = models.TextField()
    blog_post = models.TextField()
    banner = models.ImageField(blank=True, null = True, upload_to= 'images/')
    def __str__(self):
        return self.title
