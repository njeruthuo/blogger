from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # path('', views.PostListView.as_view(), name='post_list'),
    path('', views.post_list, name='post_list'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail, name='post_detail'),
    path('delete/comment/<int:comment_id>/',
         views.comment_delete, name='delete'),
]
