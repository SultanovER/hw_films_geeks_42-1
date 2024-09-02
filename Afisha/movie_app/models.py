from django.db import models

class AbstractModel(models.Model):
    class Meta:
        abstract = True
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Category(AbstractModel):
    view_count = models.IntegerField(default=0)

class SearchTag(AbstractModel):
    class Meta:
        verbose_name = 'Поисковые слова'
        verbose_name_plural = 'Поисковые слова'

class Director(models.Model):
    class Meta:
        verbose_name = 'Режиссёр'
        verbose_name_plural = 'Режиссёры'
    name = models.CharField(max_length=100)
    tags = models.ManyToManyField(SearchTag, blank=True, verbose_name='Поисковые слова')

    def __str__(self):
        return self.name
    def rating(self):
        return 0

class Movie(models.Model):
    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(SearchTag, blank=True, verbose_name='Поисковые слова')
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Описание')
    duration = models.DurationField(verbose_name='Продолжительность')
    director = models.ForeignKey(Director, null=True, on_delete=models.SET_NULL, verbose_name='Режиссёр')

    def __str__(self):
        return self.title
    def rating(self):
        return 0


STAR_CHOISE = (
    (1, '*'),
    (2, '**'),
    (3, '***'),
    (4, '****'),
    (5, '*****')
)
class Review(models.Model):
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
    stars = models.IntegerField(choices=STAR_CHOISE, default=1)
    text = models.TextField(verbose_name='Отзыв')
    movie = models.ForeignKey(Movie, null=True, on_delete=models.SET_NULL, related_name='all_reviews')

    def __str__(self):
        return self.text
    
    def rating(self):
        return 0