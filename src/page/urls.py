from django.urls import path, include

from . import views

app_name = 'page'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('post/create/', views.PostCreateView.as_view(), name='create'),
    path('post/<int:pk>/update', views.PostUpdateView.as_view(), name='update'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name='delete'),
    # path('post/<str:username>', views.userPostListView, name='user-posts'),
    path('post/<str:username>', views.UserPostListView.as_view(), name='user-posts')

]
