from rest_framework import serializers
from .models import Director, Movie, Review, Category, SearchTag
from rest_framework.exceptions import ValidationError


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchTag
        fields = '__all__'

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
    
class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=2, max_length=100)
    description = serializers.CharField(required=False)
    duration = serializers.DurationField()
    tags = serializers.ListField(child=serializers.IntegerField())
    director_id = serializers.IntegerField(min_value=1)

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id['category_id'])
        except Category.DoesNotExist:
            raise ValidationError('Category does not exists!')
        return category_id
    def validate_tags(self, tags):
        tags_from_db = SearchTag.objects.filter(id__in=tags)
        if len(tags_from_db) != len(tags):
            raise ValidationError('Tags does not exists!')
        return tags

class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=2, max_length=100)
    tags = serializers.ListField(child=serializers.IntegerField())

    def validate_tags(self, tags):
        tags_from_db = SearchTag.objects.filter(id__in=tags)
        if len(tags_from_db) != len(tags):
            raise ValidationError('Tags does not exists!')
        return tags

class ReviewValidateSerializer(serializers.Serializer):
    stars = serializers.IntegerField()
    text = serializers.CharField(required=False)
    movie_id = serializers.IntegerField(min_value=1)

