from django.urls import path

from . import views

from django.views.generic import TemplateView

app_name = "base"

urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),
    path("firstlogin/", views.FirstLoginView.as_view(), name="first_login"),
    path("profile/", views.profile, name="profile"),
    path("", views.google_login),
    path("preference/", views.preference, name="preference"),
    path('home/create', views.create_offer, name='create_offer'),
    path("transfer/", views.first_login, name="transfer"),
    path('home/<int:pk>/', views.show_task, name='TaskView'),
    path('volunteer/', views.VolunteerView.as_view(), name='Volunteer'),
    path('donate/', views.DonateView.as_view(), name='Donate'),
    path("donate/transaction/<int:pk>/", views.transaction, name="transaction"),
    path("<args>/donate/success/<int:pk>/", views.success, name="success"),
    path("volunteer/confirmation<int:pk>/", views.vsuccess, name="vsuccess"),
    path("about", views.AboutView.as_view(), name="about"),
    path("profile/edit", views.edit_profile, name="edit"),
    path("profile/edit-profile", views.save_edit, name="edit_profile"),
    path("schedule/", views.schedule, name='schedule'),
    path('schedule/<int:pk>/', views.accepted_task, name='accepted_task'),
    path('submitted-events/', views.submitted_events, name='submitted_events'),
    path('submitted-events/<int:pk>/', views.submitted_volunteer_view, name='submitted_volunteer_view'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
]