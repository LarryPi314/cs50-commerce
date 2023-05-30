from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("postlisting/<str:name>", views.post_listing, name="postlisting"),
    path("displaylisting/<int:identifier>", views.display_listing, name="displaylisting"),
    path("watchlist/<str:name>", views.watchlist, name="watchlist"),
    path("placebid", views.place_bid, name="placebid"),
    path("postcontent", views.post_comment, name="postcomment")
]