from django.contrib import admin
from django.urls import path, include
from movie_app import views
from movie_app.views import MovieListView, DirectorListView
from . import wsgi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/movie_app/movies/', include('movie_app.urls')),
    path('api/v1/movie_app/reviews/', include('movie_app.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/movie_app/directors/<int:id>/', views.director_detail_api_view),
    path('api/v1/movie_app/movies/<int:id>/', views.movie_detail_api_view),
    path('api/v1/movie_app/reviews/<int:id>/', views.review_detail_api_view),
    path('api/v1/movie_app/movies/reviews/', MovieListView.as_view(), name='movie-list-with-reviews'),
    path('api/v1/movie_app/directors/', include('movie_app.urls')),
]
urlpatterns += wsgi.urlpatterns
