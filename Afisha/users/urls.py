from users import views
from django.urls import path

urlpatterns = [
    path('registration/', views.register_api_view),
    path('authorization/', views.AuthAPIView.as_view()),
]
