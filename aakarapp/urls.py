from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("index.html", views.home, name="home_html"),
    path("register", views.register_cr, name="register_cr"),
    path("login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("profile", views.update_profile, name="update_profile"),
    path("tasks", views.tasks_page, name="tasks_page"),
    path("leaderboard.html", views.leaderboard, name="leaderboard"),
    path("leaderboard", views.leaderboard, name="leaderboard_short"),
    path("contact", views.contact, name="contact"),
    path("about.html", views.static_page, {"page": "about"}, name="about_page"),
    path("roles.html", views.static_page, {"page": "roles"}, name="roles_page"),
    path("incentives.html", views.static_page, {"page": "incentives"}, name="incentives_page"),
    path("faq.html", views.static_page, {"page": "faq"}, name="faq_page"),
    path("team.html", views.static_page, {"page": "team"}, name="team_page"),
    path("day.html", views.static_page, {"page": "day"}, name="day_page"),
    path("password-reset/", views.PortalPasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", views.PortalPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password-reset/confirm/<uidb64>/<token>/", views.PortalPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password-reset/complete/", views.PortalPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
