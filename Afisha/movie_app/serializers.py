from rest_framework import serializers
from .models import Director, Movie, Review, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name'.split()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        depth = 1

class MovieSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    all_reviews = ReviewSerializer(many=True)
   
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = 'id title director description duration category tags all_reviews rating average_rating'.split()
        depth = 1
    def get_average_rating(self, obj):
        return obj.rating()

    
class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = 'id name movies_count'.split()
        depth = 1

    def get_movies_count(self, obj):
        return obj.movie_set.count()

