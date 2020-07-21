from django.urls import path
from . import views
app_name='blog'

urlpatterns = [
    path('',views.PostListView.as_view(),name='post_list'),
    path('post/create',views.PostCreateView.as_view(),name='post_create'),
    path('drafts/',views.DraftList.as_view(),name='draft_list'),
    path('post/publish/<int:pk>',views.post_publish,name='publish'),
    path('post/detail/<int:pk>',views.PostDetailView.as_view(),name='post_detail'),
    path('post/update/<int:pk>',views.PostUpdateView.as_view(),name='post_update'),
    path('post/delete/<int:pk>',views.PostDeleteView.as_view(),name='post_delete'),
    path('comment/add/<int:pk>',views.add_comment_to_post,name='add_comment'),
    path('comment/approve/<int:pk>',views.comment_approve,name='approve_comment'),
    path('comment/delete/<int:pk>',views.comment_delete,name='delete_comment'),

]
