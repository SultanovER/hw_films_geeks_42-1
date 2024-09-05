from movie_app import views
from django.urls import path

urlpatterns = [
    path('', views.MovieListCreateAPIView.as_view()),
    path('movies/<int:id>/', views.movie_detail_api_view),
    path('directors/<int:id>/', views.director_detail_api_view),
    path('reviews/<int:id>/', views.review_detail_api_view),
    path('categories/', views.CategoryListAPIView.as_view()),
    path('categories/<int:id>/', views.CategoryDetailAPIView.as_view()),
    path('tags/', views.TagModelViewSet.as_view({
        'get': 'list', 'post': 'create'
    })),
    path('tags/<int:id>/', views.TagModelViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
    }))
]
