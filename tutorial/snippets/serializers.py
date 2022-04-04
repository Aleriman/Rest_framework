from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.contrib.auth.models import User
# Create your models here.
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0],item[0])for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


#Serializar = Permiten que datos complejos como consultas e instancias de modelos, se conviertan en tipos de datos nativos de python que luego se pueden representar facilmente en u otros tipos de contenido JSON. Tambien brinda desserializacion por lo que los datos analizados se vuelvan a convertir a datos complejos, despues de validar primero los datos entrantes.

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username')
	highlight = serializers.HyperlinkedIdentityField(view_name='snippets-highlight', format='html')
	url = serializers.HyperlinkedIdentityField(view_name = 'snippets-detail',)
	
	class Meta:
		model = Snippet
		fields = ['url', 'id', 'highlight', 'title', 'code', 'owner', 'linenos', 'language', 'style']	

class UserSerializer(serializers.HyperlinkedModelSerializer):
	snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippets-detail', read_only=True)
	url = serializers.HyperlinkedIdentityField(view_name = 'snippets-detail',)
	class Meta:
		model = User
		fields = ['url', 'id', 'username', 'snippets']
	"""
	1os pasos de serialización, usando la clase serializer.	
	
	id = serializers.IntegerField(read_only=True)
	title = serializers.CharField(required=False, allow_blank=True, max_length=100)
	code = serializers.CharField(style={'base_template': 'textarea.html'})
	linenos = serializers.BooleanField(required=False)
	language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
	style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
	
	def create(self, validated_data):
		#Crea y retorna una nueva instancia 'Snippet', dado los datos validados.
		return Snippet.objects.create(**validated_data)
	
	def update(self, instance, validated_data):
		#Actualiza y retorna una instancia 'Snippet' existente, dado los datos validados
		instance.title = validated_data.get('title', instance.title)
		instance.code = validated_data.get('code', instance.code)
		instance.linenos = validated_data.get('linenos', instance.linenos)
		instance.language = validated_data.get('language', instance.language)
		instance.style = validated_data.get('style', instance.style)
		instance.save()
		return instance
	"""
