				Create and Connect with MS SQL and Document with Swagger + Token-based-authentication

-------------------------------------------Create and Connect with MS SQL-----------------------------------------------

01. Make a new project folder

	mkdir main_project
	cd main_project

02. Create a virtual environment inside the project folder

	python -m venv venv

03. Activate the virtual environment

	Windows: venv\Scripts\activate
	Linux/macOS: source venv/bin/activate

04. Install Django inside Project folder

	pip install django

05. Create Start the Django Project

	django-admin startproject Project . # create project same dir

##. Run Your Project

	python manage.py runserver

06. Let's wire up the API URLs. On to djangorest/urls.py:

	path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

07. Add 'rest_framework' to INSTALLED_APPS. In djangorest/settings.py

	 'rest_framework',

08. Install Django REST framework

	pip install djangorestframework

09. Create an app- djangorestapi 

	python manage.py startapp djangorestapi

10. Add 'djangorestapi' to INSTALLED_APPS. In djangorest/settings.py

	'djangorestapi',


11. inside djangorestapi app model.py create model(Complex Data)-->

	# Create your models here.
	class Aiquest(models.Model):
		teacher_name = models.CharField(max_length=25)
		course_name = models.CharField(max_length=20)
		course_duration = models.IntegerField()
		seat = models.IntegerField()


##-----------------------------------------------Connect MS SQL------------------------------------------>
	# install:

		pip install django-mssql-backend
		pip install mssql-django


	# inside djangorest/settings.py  add fields to connect with mssql:

		DATABASES = {
		'default': {

				# 'ENGINE': 'django.db.backends.sqlite3',
				# 'NAME': BASE_DIR / 'db.sqlite3',

				'ENGINE': 'mssql',
				'NAME': 'djangoTest',
				'USER': 'sa',
				'PASSWORD': 'dellvostro',
				'HOST': 'VOSTRO3910\\SQLEXPRESS',
				'PORT': '',

				'OPTIONS': {
					'driver': 'ODBC Driver 17 for SQL Server',
					'trust_server_certificate': 'yes',
				},
			}
		}

## make migration to convert model into exactly into sql query 

12. Make migration:

	python manage.py makemigrations
	## now migrate
	python manage.py migrate

13.  Register  models in djangorestapi/admin.py: 
	
	import model: from . models import Aiquest
	register like: @admin.register(Aiquest)
				   #register sequentially so view as like this sequentially-
				   class AiquestAdmin(admin.ModelAdmin):
					  list_display = ['id','teacher_name','course_name','course_duration','seat']


##. Create superuser: python manage.py createsuperuser ------------------------------------------------->


14. Create a serializer in djangorestapi/serializers.py

	serializers.py

	# import serializer: 
		from rest_framework import serializers
		from rest_framework import serializers
		from .models import Aiquest

	# create serializer class:

		class AiquestSerializer(serializers.ModelSerializer):
			class Meta:
				model = Aiquest
				fields = ['teacher_name', 'course_name', 'course_duration', 'seat']


	[ # manual process: 
		class AiquestSerializer(serializers.Serializer):
			teacher_name = serializers.CharField(max_length=25)
			course_name = serializers.CharField(max_length=20)
			course_duration = serializers.IntegerField()
			seat = serializers.IntegerField()

			def create(self, validated_data):
				# Create a new Aiquest instance
				aiquest_instance = Aiquest(
					teacher_name=validated_data['teacher_name'],
					course_name=validated_data['course_name'],
					course_duration=validated_data['course_duration'],
					seat=validated_data['seat']
				)
				# Save the instance to the database
				aiquest_instance.save()
				return aiquest_instance
	]

15. Create  views: Based on [API Views] views will be different  Below one is for [Class Based Api View]---

	from django.shortcuts import render
	from . models import Aiquest
	from . serializers import AiquestSerializer
	from rest_framework.views import APIView
	from rest_framework.response import Response
	from rest_framework import status

	# Create your views here.

	class AiquestCreate(APIView):

		#-------------------    GET     -----------------------

		def get(self, request, pk= None, format= None ):
			id = pk
		#  for specif id
			if id is not None:
				try:
					ai = Aiquest.objects.get(id=id)
					serializer = AiquestSerializer(ai)
					return Response(serializer.data)
				except Aiquest.DoesNotExist:
					# return Response({"msg": " Not found"}, status=status.HTTP_404_NOT_FOUND)    or
					return Response([], status=status.HTTP_200_OK)
			
		# for all data 
			# import and store complex data into one variable from model:
			ai = Aiquest.objects.all()

			# convert/serialize into python dict:(import and use from serializers.py)
			# many= True : used because of more than one object inside AiquestSerializer
			serializer = AiquestSerializer(ai, many=True)

			# convert python dict to JSON and return :
			return Response(serializer.data)
		

		#-------------------    POST     -----------------------
		
		def post(self, request, format= None ):
			serializer = AiquestSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response({"msg":"Successfully Insert Data"})
			return Response(serializer.errors)
		

		#-------------------     PUT     -----------------------

		def put(self, request, pk, format= None ):
			id = pk
			ai = Aiquest.objects.get(pk = id)
			# serializer = AiquestSerializer(ai, data = request.data, partial = True) # this will allow   partial update
			serializer = AiquestSerializer(ai, data = request.data) # this need to provide all field even is update one field
			if serializer.is_valid():
				serializer.save()
				return Response({"msg":"Update Data Successfully"})
			return Response(serializer.errors)

		#-------------------    PATCH     -----------------------

		def patch(self, request, pk, format= None ):
			id = pk
			ai = Aiquest.objects.get(pk = id)
			serializer = AiquestSerializer(ai, data = request.data, partial = True)
			if serializer.is_valid():
				serializer.save()
				return Response({"msg":"Partial Data Update Successfully"})
			return Response(serializer.errors)
		
		#-------------------    DELETE     -----------------------

		def delete(self, request, pk, format= None ):
			id = pk
			ai = Aiquest.objects.get(pk = id)
			ai.delete()
			return Response({"msg":"Delete Successfully"})


16. Add new API URLs. On to djangorest/urls.py:
	
	path('aiquest/', views.AiquestCreate.as_view(), name='aiquest'),
  path('aicreate/<int:pk>', views.AiquestCreate.as_view(), name='aicreate'),


	

16. Create Urls in djangorest/urls.py
	path('aiquest/', views.AiquestCreate.as_view(), name='aiquest'),
  path('aiquest/<int:pk>', views.AiquestCreate.as_view(), name='aiquest'),


17. Run and Check your API.

##----------------------------------------API Authentication  Documenting--------------------------------------->

# Add to INSTALLED_APPS in settings.py
	
		INSTALLED_APPS = [
    			...
    			'rest_framework',
    			'rest_framework.authtoken',
    			'restApi',
		]

# Add REST Framework Auth settings below of  settings.py

		REST_FRAMEWORK = {
    			'DEFAULT_AUTHENTICATION_CLASSES': [
        		'rest_framework.authentication.TokenAuthentication',
    			],
    			'DEFAULT_PERMISSION_CLASSES': [
        		'rest_framework.permissions.IsAuthenticated',
    			]
		}

#  Create View file: restApi/auth_views.py
	
	# check all codes inside of auth_views.py
	
#  Update urls In mainProject/urls.py:
	
	# imports for authentication:

	from restApi.auth_views import register_user, login_user, logout_user, change_password,forgot_password, reset_password_with_otp

	# inside urlpatterns add links for authentication

    	path('register/', register_user),
    	path('login/', login_user),
    	path('logout/', logout_user),
    	path('change-password/', change_password),
    	path('forgot-password/', forgot_password),
    	path('reset-password-otp/', reset_password_with_otp),

# in views.py import and add permission classes
	
	from rest_framework.permissions import IsAuthenticated
	from rest_framework.decorators import permission_classes

	
	@permission_classes([IsAuthenticated])


#  Makemigrations, Migrate & Create Superuser


#  check those code and match with code check auth_views, settings,models.....

from pathlib import Path
import os


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'sabbir@abc.com'
EMAIL_HOST_PASSWORD = 'jrazwbbweqxvrriz'  # this is from email , app password

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER





from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + datetime.timedelta(minutes=10)  # 10 min validity






import random
from django.core.mail import send_mail
from .models import PasswordResetOTP




##----------------------------------------API Documenting for Swagger--------------------------------------->


## Install : pip install drf-spectacular

## then add drf-spectacular to installed apps in settings.py:
	INSTALLED_APPS = [
	    # ALL YOUR APPS
	    'drf_spectacular',
	]
## register our spectacular AutoSchema with DRF and SPECTACULAR_SETTINGS  below settings.py:

	REST_FRAMEWORK = {
	    # YOUR SETTINGS
	    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
	}

	SPECTACULAR_SETTINGS = {
    	'TITLE': 'ProjectOne API ',
    	'DESCRIPTION': 'API',
    	'VERSION': '1.0.0',
    	'SERVE_INCLUDE_SCHEMA': False, 
    	'SWAGGER_UI_SETTINGS': {
        	'persistAuthorization': True,  # Keeps token in Swagger UI after login
    	},
    	'COMPONENT_SPLIT_REQUEST': True,
	}

## in urls.py add:
	from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

	urlpatterns = [
		    # Others
		    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
		    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui')
		]
## Inside view add 
	# import: from drf_spectacular.utils import extend_schema
	# for "GET","POST"
		@extend_schema(
		    methods=["GET", "POST"],
		    request=EmployeeSerializer,
		    responses=EmployeeSerializer
		)
	# for "RETRIVE","PUT","DELETE"
		@extend_schema(
		    methods=["GET", "PUT", "DELETE"],
		    request=EmployeeSerializer,
		    responses=EmployeeSerializer
		)

##----------------------------------------API Documenting (2) for Swagger--------------------------------------->


# pip install --upgrade drf-yasg
# pip install --upgrade drf-yasg[validation]

# In settings.py:

	INSTALLED_APPS = [
	   ...
	   'django.contrib.staticfiles',  # required for serving swagger ui's css/js files
	   'drf_yasg',
	   ...
	]

# In urls.py:
	# Swagger imports
	from rest_framework import permissions
	from drf_yasg.views import get_schema_view
	from drf_yasg import openapi

	# Schema View
	schema_view = get_schema_view(
	    openapi.Info(
	        title="Employee API",
	        default_version='v1',
	        description="CRUD operations for Employee",
	        contact=openapi.Contact(email="your-email@example.com"),
	    ),
	    public=True,
	    permission_classes=[permissions.AllowAny],
	)

	urlpatterns = [

	    # Swagger URLs
	    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
	]


# In views.py: 
	# Swagger 
	from drf_yasg.utils import swagger_auto_schema
	from drf_yasg import openapi

	# Add for post and put: 
	@swagger_auto_schema(method='post',request_body=YourSerializerName,operation_description="Create new Name")
	@swagger_auto_schema(method='put',request_body=YourSerializerName,operation_description="Update Name")













