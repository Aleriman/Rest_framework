from django.urls import path
from snippets import views
#Import de la parte 2 del tutorial
from rest_framework.urlpatterns import format_suffix_patterns
#Import tutorial 4
from django.urls import path, include
#Imports tutorial 6
from snippets.views import SnippetViewSet, UserViewSet
from rest_framework import renderers
from rest_framework.routers import DefaultRouter
#p3 vamos a refactorizar las urls.
"""Conectamos nuestras vistas serializadas"""

# Creamos un router y registramos nuestros conjuntos de vistas con el.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet, basename="snippets")
router.register(r'users', views.UserViewSet, basename="users")

urlpatterns = [
    path('', include(router.urls)),
    #path('snippets/', views.snippet_list),
    #path('snippets/<int:pk>/', views.snippet_detail),
    #path('snippets/', snippet_list, name='snippet-list'),
    #path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
    #path('users/', user_list, name='user-list'),
    #path('users/<int:pk>/', user_detail, name='user-detail'),
    #Se crean en el tutorial parte 5
    #Reescribimos como nos dice en el tutorial 6
    #path('', api_root),
    #path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),   

]
#Agregamos un conjunto de format_suffix_patterns ademas de las URLs existentes
#urlpatterns = format_suffix_patterns(urlpatterns)
#Tutorial 6

