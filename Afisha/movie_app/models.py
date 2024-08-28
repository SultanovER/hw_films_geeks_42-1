from django.db import models

class Director(models.Model):
    class Meta:
        verbose_name = 'Режиссёр'
        verbose_name_plural = 'Режиссёры'
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Описание')
    duration = models.DurationField(verbose_name='Продолжительность')
    director = models.ForeignKey(Director, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
    text = models.TextField(verbose_name='Отзыв')
    movie = models.ForeignKey(Movie, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.text