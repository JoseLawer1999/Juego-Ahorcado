from django.db import models
import random

# Create your models here.


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Palabra(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    texto = models.CharField(max_length=100)
    pista = models.TextField()

    def __str__(self):
        return self.texto


class Jugador(models.Model):
    # nickname = models.CharField(max_length=100, unique=True)
    nickname = models.CharField(max_length=50)
    score = models.IntegerField(default=0)
    acertijos = models.IntegerField(default=5)

    def __str__(self):
        return self.nickname
