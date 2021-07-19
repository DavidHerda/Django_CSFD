from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    title_unidecode = models.CharField(max_length=200)
    year = models.IntegerField()
    actors = models.ManyToManyField('Actor')

    def __str__(self):
        return self.title    

    class Meta:
        ordering = ['id']

class Actor(models.Model):
    name = models.CharField(max_length=200)
    name_unidecode = models.CharField(max_length=200)
    movies = models.ManyToManyField('Movie')

    def __str__(self):
        return self.name