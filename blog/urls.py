from django.urls import path
from blog import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.CreatePostView.as_view(), name='post_new'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/remove', views.PostDeleteView.as_view(), name='post_remove'),
    path('drafts/', views.DraftListView.as_view(), name='draft'),

    path('post/<int:pk>/comment', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove', views.comment_remove, name='comment_remove'),
    path('comment/<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    path('post/<int:pk>/approve', views.post_publish, name='post_approve'),
    path('post/search', views.search_post, name='search_post')
]