from django.urls import path,include
from . import views
from comments import views as comment_views
from django.contrib.auth import views as auth_views
from jobs import views as jobs_views
from .views import user_profile


urlpatterns = [
    path("",views.home,name="home"),
    path('signup', views.signup, name='signup'),
    path("login",views.login_view,name="login"),
    path("logout",views.logout_view,name="logout"),
    path("welcome",views.welcome,name="welcome"),
    path("new",views.new_stories,name="new"),
    path("past",views.past_stories,name="past"),
    path("jobs",jobs_views.jobs,name="jobs"),
    path("comments",comment_views.show_comments,name="comments"),
    path("submit",views.submit,name="submit"),
    path("bookmark",views.bookmark,name="bookmark"),
    path("item/<int:id>/", views.item, name="item"),  
    path("upvote/<int:submission_id>/", views.upvote, name="upvote"),
    path("user/<str:username>/", user_profile, name="user_profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("search/", views.search, name="search"),
    path("edit/<int:id>/", views.edit_submission, name="edit_submission"),
    path("delete/<int:id>/", views.delete_submission, name="delete_submission"),
    path("domain/", views.domain_filter, name="domain_filter")
    

]
    
  
