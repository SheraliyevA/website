from django.shortcuts import render,get_object_or_404,redirect
from django.template.defaultfilters import slugify
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from .forms import *
from taggit.models import Tag
from django.db.models import Q
from django.http import HttpResponseNotFound

def handler404(request,exception):
    return HttpResponseNotFound("<strong> Ma'lumot topilmadi </strong>")


def home(request):
    posts = Post.objects.order_by('-published')
    search=request.GET.get('search')
    if search:
         posts=Post.objects.filter(Q(title__icontains=search) & Q(description__icontains=search) )
    
    # Paginator
    contact_list = Post.objects.all()
    paginator = Paginator(contact_list, 3) # Show 3 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(request.GET)

    common_tags = Post.tags.most_common()[:10]
    form = PostForm(request.POST)
    if form.is_valid():
        newpost = form.save(commit=False)
        newpost.slug = slugify(newpost.title)
        newpost.save()
        # Without this next line the tags won't be saved.
        form.save_m2m()
    context = {
        'posts':posts,
        'common_tags':common_tags,
        'form':form,
        'page_obj':page_obj
    }
    return render(request, 'home.html', context)
    

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    similar_posts = Post.objects.filter(tags__in=post.tags.all()).exclude(id=post_id)[:3]
    
    return render(request, 'post_detail.html', {'post': post, 'similar_posts': similar_posts})

def getAbout(request,slug):
    post=get_object_or_404(Post,slug=slug)
    comments = post.comments.all()

    comments = post.comments.filter(active=True)
    new_comment = None
    comment_form=CommentForm()
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            # redirect to same page and focus on that comment
            return redirect('/')
        else:
            comment_form = CommentForm()

    if post:
	    post.views=post.views+1
	    post.update_views()
    context={
        'post':post,
        'comments': comments,'comment_form':comment_form
    }
    return render(request,'detail.html',context)
        
def delete(request,id):
    news=Post.objects.get(id=id)
    news.delete()
    return redirect('home')

def tagged(request,slug):
    tag=get_object_or_404(Tag,slug=slug)
    posts=Post.objects.filter(slug=slug)
    context={
        'tag':tag,
        'posts':posts
    }
    return render(request,'home.html',context)


def signup(request):
	form=UserForm()
	if request.method=='POST':
		form=UserForm(data=request.POST,files=request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'The post has been created successfully.')
			return redirect('home')
		messages.error(request, 'Please correct the following errors:')
		return render(request,'signup.html',{'form':form})
	return render(request,'signup.html',{'form':form})


def Login(request):
	login_form=LoginForm()
	if request.method=='POST':
		login_form=LoginForm(data=request.POST)
		if login_form.is_valid():
			username=request.POST.get('username')
			password=request.POST.get('password')
			user=authenticate(username=username,password=password)

			if user is not None	:
				login(request,user)
				return redirect('home')
		return	render(request,'login.html',{'login_form':login_form})
	return	render(request,'login.html',{'login_form':login_form})

def Logout(request):
	logout(request)
	return redirect('home')

class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if is_dislike:
            post.dislikes.remove(request.user)
        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        if not is_like: 
            post.likes.add(request.user)
        
        if is_like:
            post.likes.remove(request.user)
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

 
class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        if is_like:
            post.likes.remove(request.user)
        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if not is_dislike: 
            post.dislikes.add(request.user)
        
        if is_dislike:
            post.dislikes.remove(request.user)
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    related_posts = Post.objects.filter(tags__in=post.tags.all()).exclude(id=post.id)[:3]
    return render(request, 'detail.html', {'post': post, 'related_posts': related_posts})

def reply_page(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get('post_id')  # from hidden input
            parent_id = request.POST.get('parent')  # from hidden input
            post_url = request.POST.get('post_url')  # from hidden input
            reply = form.save(commit=False)
    
            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()
            return redirect(post_url +'#'+str(reply.id))
    return redirect("/")


