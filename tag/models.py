from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth import get_user_model

User=get_user_model()

class Post(models.Model):
    title=models.CharField(max_length=1000)
    photo=models.ImageField(upload_to='media/post/images/',default='')
    description=models.TextField()
    published=models.DateField(auto_now_add=True)
    slug=models.SlugField(unique=True,max_length=1000,blank=True,null=True)
    tags = TaggableManager() 
    views=models.IntegerField(default=100)
    no_of_likes = models.IntegerField(default=0)
    post_author=models.ForeignKey(User,related_name='author',on_delete=models.CASCADE,null=True,default=None)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')

    def update_views(self,*args,**kwargs):
        self.views=self.views+1
        super().save(*args,**kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('detail', kwargs={'id': self.id})

    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)

class LikePost(models.Model):
	
	post_id = models.CharField(max_length=500)
	username = models.CharField(max_length=100) 
	def __str__(self):
		return self.username

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")
    name=models.CharField(max_length=50)
    email=models.EmailField()
    parent=models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return self.body
    
    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)
