from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

handler404='tag.views.handler404'
urlpatterns=[
   path('',home,name='home'),
    path('/<slug:slug>/',getAbout,name='detail'),
    path('tags/<slug:slug>/',tagged,name='tagged'),
    path('signup/',signup,name='signup'),
    path('Login/',Login,name='login'),
    path('Logout/',Logout,name='logout'),
    path('del<int:id>/',delete,name='delete'),
    path('post/<int:pk>/like', AddLike.as_view(), name='like'),
    path('post/<int:pk>/dislike', AddDislike.as_view(), name='dislike'),
    path('post_detail/<int:post_id>/',post_detail,name='post_detail'),
    path('comment/reply/',reply_page, name="reply"),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
