from django.urls import path
from blog import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.CreatePostView.as_view(), name='post_new'),
    path('post/<int:pk>/update/', views.UpdatePostView.as_view(), name='post_edit'),
    path('post/<int:pk>/remove', views.DeletePostView.as_view(), name='post_remove'),
    path('drafts/', views.DraftListView.as_view(), name='draft')
]