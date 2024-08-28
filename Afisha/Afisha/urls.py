from django.contrib import admin
from django.urls import path
from movie_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/movie_app/directors/', views.director_list_api_view),
    path('api/v1/movie_app/movies/', views.movie_list_api_view),
    path('api/v1/movie_app/reviews/', views.review_list_api_view),
    path('api/v1/movie_app/directors/<int:id>/', views.director_detail_api_view),
    path('api/v1/movie_app/movies/<int:id>/', views.movie_detail_api_view),
    path('api/v1/movie_app/reviews/<int:id>/', views.review_detail_api_view),

]
