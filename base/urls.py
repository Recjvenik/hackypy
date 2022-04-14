from django.urls import path
from . import views

urlpatterns = [
    path('', views.storyView, name='home' ),
    path('create-comments/<int:pk>/', views.createComments, name='create-comments'),
    path('reply-comments/<int:pk>/', views.replyComment, name='reply-comments'),
    path('create-post', views.createPost, name='create-post'),
    path('vote-post/<int:pk>/', views.postVote, name='vote' ), 
    path('search/', views.searchPost, name='search')
]