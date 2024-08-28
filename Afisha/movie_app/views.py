from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Director, Movie, Review
from rest_framework import status
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer

@api_view(['GET'])
def director_detail_api_view(request, id):
    director = Director.objects.get(id=id)
    data = DirectorSerializer(director).data
    return Response(data=data)

@api_view(['GET'])
def movie_detail_api_view(request, id):
    movie = Movie.objects.get(id=id)
    data = MovieSerializer(movie).data
    return Response(data=data)

@api_view(['GET'])
def review_detail_api_view(request, id):
    review = Review.objects.get(id=id)
    data = ReviewSerializer(review).data
    return Response(data=data)

@api_view(http_method_names=['GET'])
def director_list_api_view(request):
    directors = Director.objects.all()
    list_ = DirectorSerializer(instance=directors, many=True).data
    return Response(data=list_, status=status.HTTP_200_OK)

@api_view(http_method_names=['GET'])
def movie_list_api_view(request):
    movies = Movie.objects.all()
    list_ = MovieSerializer(instance=movies, many=True).data
    return Response(data=list_, status=status.HTTP_200_OK)

@api_view(http_method_names=['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    list_ = ReviewSerializer(instance=reviews, many=True).data
    return Response(data=list_, status=status.HTTP_200_OK)


