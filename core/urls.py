from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('follow', views.follow, name='follow'),
    path('search', views.search_two, name='search-two'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('like-post', views.like_post, name='like-post'),
    path('like-post2', views.like_post2, name='like-post2'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),

    #added
    # path('subject', views.subject, name='subject'),
    # path('sub-subject', views.sub_subject, name='sub_subject'),
    path('topic', views.topic, name='topic'),
    path('new_page', views.new_page, name='new_page'),
    path('create-pod', views.create_pod, name='create-pod'),
    # path('search', views.search_two, name='search-two'),
    # path('pod-detail/', views.pod_detail, name='pod_detail'),
    path('join-pod', views.join_pod, name='join-pod'),
]