from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Director, Movie, Review
from rest_framework import status, generics
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer, MovieValidateSerializer, DirectorValidateSerializer, ReviewValidateSerializer

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
        data = DirectorSerializer(director).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = DirectorValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        director.name = request.data.get("name")
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
        serializer = MovieValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie.title = serializer._validated_data.get("title")
        movie.duration = serializer._validated_data("duration")
        movie.description = serializer._validated_data("description")
        movie.director = serializer._validated_data("director")
        movie.tags = serializer._validated_data("tags")
        movie.save()
        return Response(data=MovieSerializer(movie).data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Reviews not found!'})
    
    if request.method == 'GET':
        data = ReviewSerializer(review).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review.stars = serializer.validated_data.get("stars")
        review.text = serializer.validated_data.get('text')
        review.movie = serializer.validated_data.get('movie')
        review.save()
        return Response(data=ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    data = ReviewSerializer(review).data
    return Response(data=data)

@api_view(http_method_names=['GET', 'POST'])
def director_list_create_api_view(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        list_ = DirectorSerializer(instance=directors, many=True).data
        return Response(data=list_, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=400, data=serializer.errors)
        name = serializer.validated_data.get("name")
        tags = serializer.validated_data.get("tags")
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
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=400, data=serializer.errors)
        title = serializer.validated_data.get("title")
        duration = serializer.validated_data.get("duration")
        description = serializer.validated_data.get("description")
        director = serializer.validated_data.get("director")
        tags = serializer.validated_data.get("tags")
        
        movie = Movie.objects.create(
            title=title,
            duration=duration,
            description=description,
            director=director.id
        )
        movie.tags.set(tags)
        movie.save()
        return Response(data=MovieSerializer(movie).data, status=status.HTTP_201_CREATED)
    
    

@api_view(http_method_names=['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        list_ = ReviewSerializer(instance=reviews, many=True).data
        return Response(data=list_, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=400, data=serializer.errors)
        stars = serializer.validated_data.get("stars")
        text = serializer.validated_data.get("text")
        movie = serializer.validated_data.get("movie")
        
        review = Review.objects.create(
            stars=stars,
            text=text,
            movie=movie.id
        )
        review.save()
        return Response(data=ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
    
    

