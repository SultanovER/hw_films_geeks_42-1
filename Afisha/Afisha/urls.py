from django.contrib import admin
from django.urls import path
from movie_app import views
from movie_app.views import MovieListView, DirectorListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/movie_app/movies/', views.movie_list_api_view),

    path('api/v1/movie_app/reviews/', views.review_list_api_view),
    path('api/v1/movie_app/directors/<int:id>/', views.director_detail_api_view),
    path('api/v1/movie_app/movies/<int:id>/', views.movie_detail_api_view),
    path('api/v1/movie_app/reviews/<int:id>/', views.review_detail_api_view),
    path('api/v1/movie_app/movies/reviews/', MovieListView.as_view(), name='movie-list-with-reviews'),
    path('api/v1/movie_app/directors/', DirectorListView.as_view(), name='director-list'),

]
