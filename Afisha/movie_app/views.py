from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Director, Movie, Review, Category, SearchTag
from rest_framework import status, generics
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer, MovieValidateSerializer, DirectorValidateSerializer
from .serializers import ReviewValidateSerializer, CategorySerializer, TagSerializer
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet


class TagModelViewSet(ModelViewSet):
    queryset = SearchTag.objects.all()
    serializer_class = TagSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'

class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('total', data)
        ]))

class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPagination

class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

class MovieDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    def get(self):
        try:
            return Movie.objects.get(id=self.kwargs['id'])
        except Movie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Movie not found!'})

    def put(self, request, *args, **kwargs):
        movie = self.get_object()
        serializer = MovieValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie.title = serializer._validated_data.get("title")
        movie.duration = serializer._validated_data("duration")
        movie.description = serializer._validated_data("description")
        movie.director = serializer._validated_data("director")
        movie.tags = serializer._validated_data("tags")
        movie.save()
        return Response(data=MovieSerializer(movie).data, status=status.HTTP_201_CREATED)
    def delete(self, request, *args, **kwargs):
        movie = self.get_object()
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DirectorDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    def get(self):
        try:
            return Director.objects.get(id=self.kwargs['id'])
        except Director.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Director not found!'})
    def put(self, request, *args, **kwargs):
        director = self.get_object()
        serializer = DirectorValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        director.name = request.data.get("name")
        director.tags = request.data.get("tags")
        director.save()
        return Response(data=DirectorSerializer(director).data, status=status.HTTP_201_CREATED)
    def delete(self, request, *args, **kwargs):
        director = self.get_object()
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MovieListCreateAPIView(ListAPIView):
    queryset = movies = Movie.objects.select_related(
        'category'
    ).prefetch_related(
        'tags',
        'all_reviews'
    ).filter(is_active=True)
    serializer_class = MovieSerializer

    def post(self, request, *args, **kwargs):
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
    def get(self, *args, **kwargs):
        movies = Movie.objects.select_related('category').prefetch_related('tags', 'all_reviews').all()
        list_ = MovieSerializer(instance=movies, many=True).data
        return Response(data=list_, status=status.HTTP_200_OK)
    
class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    review = Review.objects.get(id=id)
    def get(self):
        try:
            Review.objects.get(id=id)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Review not found!'})
    def put(self, request, *args, **kwargs):
        review = self.get_object()
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review.stars = serializer.validated_data.get("stars")
        review.text = serializer.validated_data.get('text')
        review.movie = serializer.validated_data.get('movie')
        review.save()
        return Response(data=ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
       
    def delete(self, *args, **kwargs):
        review = self.get_object()
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class DirectorCreateAPIView(ListAPIView):
    queryset = directors = Director.objects.select_related(
        'category'
    ).prefetch_related(
        'tags',
        'all_reviews'
    ).filter(is_active=True)
    serializer_class = DirectorSerializer
    def post(self, request, *args, **kwargs):
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
    def get(self, *args, **kwargs):
        directors = Director.objects.all()
        list_ = DirectorSerializer(instance=directors, many=True).data
        return Response(data=list_, status=status.HTTP_200_OK)

    

class DirectorListView(generics.ListAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
