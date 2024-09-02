from django.contrib import admin
from .models import Director, Movie, Review, Category, SearchTag

admin.site.register(Director)
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(SearchTag)