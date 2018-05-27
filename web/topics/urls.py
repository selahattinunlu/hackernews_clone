from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('topics/new', views.TopicCreateView.as_view(), name='topics_create'),
    path('topics/<slug:slug>', views.TopicDetailView.as_view(), name='topics_detail'),
    path('topics/<int:id>/upvote', views.upvote, name='topics_upvote'),
    path('topics/<int:id>/comments', views.CommentCreateView.as_view(), name='topics_comments_create'),
    path('comments/<int:comment_id>', views.CommentView.as_view(), name='topics_comments')
]
