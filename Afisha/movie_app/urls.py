from movie_app import views
from django.urls import path

urlpatterns = [
    path('', views.movie_list_create_api_view),
    path('<int:id>/', views.movie_detail_api_view),
    path('<int:id>/', views.director_detail_api_view),
    path('<int:id>/', views.review_detail_api_view),
]
