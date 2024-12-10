from django.urls import path
from .import views


urlpatterns = [
    # Parte del Menu en la rustas
    path('', views.index, name='inicio'),
    path('Ayuda/', views.ayuda, name='ayuda'),

    # Parte del juego en las rutas
    path('Iniciar/', views.iniciar_juego, name='iniciar_juego'),
    path('Jugando Ahorcado/', views.jugar, name='jugando'),
    # path('Reiniciar/', views.reiniciar_juego, name='reiniciar'),
    path('ganar/', views.ganar, name='ganaste'),
    path('perder/', views.perder, name='perder'),
    path('reiniciar/', views.reiniciar, name="reiniciar"),
    path('record/', views.record, name="record"),
    #path('borrar/', views.borrar, name="borrar"),



]
