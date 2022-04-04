from django.shortcuts import render
#Imports que se añaden en el tutorial parte 4
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
#Imports del tutorial parte 1
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

#Imports del tutorial parte 2(p2)(sustituimos csrf_exempt por api_view y añadimos otros imports más. from snippets.models import Snippet y from snippets.serializers import SnippetSerializer ya esta en los imports del tutorial parte 1
from rest_framework import status
#p3 Se sustituye por from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

#Imports tutorial parte 3(p3)(Utilizamos las del apartado 1 y 2 ademas de las siguientes)
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics

#Imports tutorial parte 5, ademas de los imports api_view y Response 
#que ya estan añdidos en partes del tutorial anterior, añadimos:
from rest_framework.reverse import reverse
from rest_framework import renderers

#Imports del tutorial parte 6 
from rest_framework import viewsets
#Response que ya está
from rest_framework.decorators import action
from rest_framework import permissions

# Create your views here.
#csrf_exempt marca una vista como exenta de la proteccion garantizada por el middleware CSRF (Cross Site Request Forgery proteccion = Protección contra falsificación de solicitudes entre sitios).
#p2 Lo voy a sustituir @csrf_exempt por @api_view que es un decorador para trabajar con vistas basadas en funciones.
#Tutorial parte 2(Agregar sufijos de formato opcionales a nuestra URL)
"""p3 vamos a rescribir SnippetList 
@api_view(['GET','POST'])
def snippet_list(request, format = None):
	Lista todos los fragmento de codigo, o crea un nuevo fragmento(snippet).
	if request.method == 'GET':
		snippets = Snippet.objects.all()
		serializer = SnippetSerializer(snippets, many=True)
		#p2 Cambiamos JsonResponse por:
		#return JsonResponse(serializer.data, safe=False)
		return Response(serializer.data)

	elif request.method == 'POST':
		#p2 Quitamos la siguiente linea (comentada)
		#data = JSONParser().parse(request)
		serializer = SnippetSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			#p2 Quitamos la siguiente linea y escribimos lo siguiente:
			#return JsonResponse(serializer.data, status=201)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		#p2 Sustituimos esta linea por:
		#return JsonResponse(serializer.errors, status=400)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
"""Parte 3-2 del tutorial, el codigo escrito abajo va a ser sustituido
class SnippetList(APIView):
	
	Lista todos los fragmentos, o crea un nuevo fragmento
	
	def get(self, request, format=None):
		snippets = Snippet.objects.all()
		serializer = SnippetSerializer(snippets, many=True)
		return Response(serializer.data)
	
	def post(self, request, format=None):
		serializer = SnippetSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
#p2 Sustituimos csrf_exempt por api_view
#@api_view(['GET', 'PUT', 'DELETE'])"""

""" Tutorial 3-3 vamos a seguir reduciendo codigo usando vistas genericas basadas en clases
class SnippetList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)
"""

	
"""p3 vamos a rescribir def snippet_detail(request, pk, format = None):
	
	Recuperar, actualizar o eliminar un fragmento(snippet).
	
	try:
		snippet = Snippet.objects.get(pk=pk)
	except Snippet.DoesNotExist:
		#p2 Sustituimos HttpResponse por Response
		#return HttpResponse(status=404)
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = SnippetSerializer(snippet)
		#p2 Sustituimos JsonResponse por Response
		#return JsonResponse(serializer.data)
		return Response(serializer.data)

	elif request.method == 'PUT':
		#p2 Quitamos data=JSONParser
		#data = JSONParser().parse(request)
		serializer = SnippetSerializer(snippet, data=data)
		if serializer.is_valid():
			serializer.save()
			#p2 Sustituimos los JsonResponse por Response
			#return JsonResponse(serializer.data)
			return Response(serializer.data)
		#return JsonResponse(serializer.errors, status=400)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		snippet.delete()
		#p2 Sustituimos por Response
		#return HttpResponse(status=204)
		return Response(status=status.HTTP_204_NO_CONTENT)
"""
"""
#Tutorial parte 5
@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		'snippets': reverse('snippet-list', request=request, format=format)
	})
"""
""" Vamos a reemplazar estas tres vistas creando una sola clase. Tutorial parte 6
class SnippetHighlight(generics.GenericAPIView):
	queryset = Snippet.objects.all()
	renderer_classes = [renderers.StaticHTMLRenderer]
	
	def get(self, request, *args, **kwargs):
		snippet = self.get_object()
		return Response(snippet.highlighted)

# Heredamos de generics
class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer
	#Tutorial parte 4
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

# Heredamos de generics
class SnippetList(generics.ListCreateAPIView):
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer
	#Tutorial parte 4
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	#Asociacion de fragmentos con usuarios Tutorial 4
	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)
"""
class SnippetViewSet(viewsets.ModelViewSet):
	#Automaticamente proporcionan las acciones de: listar, crear, recuperar, actualizar y
	# destuir. Adicionalmente proporciona una accion de destacado extra.
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
	
	@action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
	def highlight(self, request, *args, **kwargs):
		snippet = self.get_object()
		return Response(snippet.highlighted)
		
	def perform_created(self, serializer):
		serializer.save(owner=self.request.user)
"""Parte 3-2 Sustituimos el codigo que esta abajo
class SnippetDetail(APIView):
	
	Recuperar, actualizar o eliminar un fragmento(snippet).
	
	def get_object(self, pk):
		try:
			return Snippet.objects.get(pk=pk)
		except Snippet.DoesNotExist:
			raise Http404
	
	def get(self, request, pk, format=None):
		snippet = self.get_object(pk)
		serializer = SnippetSerializer(snippet)
		return Response(serializer.data)
	
	def put(self, request, pk, format=None):
		snippet = self.get_object(pk)
		serializer = snippetSerializer(snippet, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, pk, format=None):
		snippet = self.get_object(pk)
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
"""
"""Tutorial 3-3 vamos a seguir reduciendo codigo con vistas genericas basadas en clases.
class SnippetDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)
"""

#Tutorial parte 4 creacion de la vista userlist
#Tutorial parte 6 vamos a reescribir la vista userlist
"""class UserList(viewsets.ReadOnlyModelViewSet):
	#Con ReadOnlyModelViewSet estas vistas automaticamente 
	#propoprcionan las acciones de listar y recuperar
	queryset = User.objects.all()
	serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
"""


class UserViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
