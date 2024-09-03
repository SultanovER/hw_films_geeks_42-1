from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Director, Movie, Review
from rest_framework import status, generics
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer

class DirectorListView(generics.ListAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer



@api_view(['GET', 'PUT', 'DELETE'])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Director not found!'})
    
    if request.method == 'GET':
        data = MovieSerializer(director).data
        return Response(data=data)
    elif request.method == 'PUT':
        director.name = request.data.get("title")
        director.tags = request.data.get("tags")
        director.save()
        return Response(data=DirectorSerializer(director).data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    data = DirectorSerializer(director).data
    return Response(data=data)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Movie not found!'})
    
    if request.method == 'GET':
        data = MovieSerializer(movie).data
        return Response(data=data)
    elif request.method == 'PUT':
        movie.title = request.data.get("title")
        movie.duration = request.data.get("duration")
        movie.description = request.data.get("description")
        movie.director = request.data.get("director")
        movie.tags = request.data.get("tags")
        movie.save()
        return Response(data=MovieSerializer(movie).data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def review_detail_api_view(request, id):
    review = Review.objects.get(id=id)
    data = ReviewSerializer(review).data
    return Response(data=data)

@api_view(http_method_names=['GET'])
def director_list_create_api_view(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        list_ = DirectorSerializer(instance=directors, many=True).data
        return Response(data=list_, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        name = request.data.get("name")
        tags = request.data.get("tags")
        director = Movie.objects.create(
            name=name,
        )
        director.tags.set(tags)
        director.save()
        return Response(data=DirectorSerializer(director).data, status=status.HTTP_201_CREATED)
    


@api_view(http_method_names=['GET', 'POST'])
def movie_list_create_api_view(request):
    if request.method == 'GET':
        movies = Movie.objects.select_related('category').prefetch_related('tags', 'all_reviews').all()
        list_ = MovieSerializer(instance=movies, many=True).data
        return Response(data=list_, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        title = request.data.get("title")
        duration = request.data.get("duration")
        description = request.data.get("description")
        director = request.data.get("director")
        tags = request.data.get("tags")
        
        movie = Movie.objects.create(
            title=title,
            duration=duration,
            description=description,
            director=director.id
        )
        movie.tags.set(tags)
        movie.save()
        return Response(data=MovieSerializer(movie).data, status=status.HTTP_201_CREATED)
    
    

@api_view(http_method_names=['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    list_ = ReviewSerializer(instance=reviews, many=True).data
    return Response(data=list_, status=status.HTTP_200_OK)


