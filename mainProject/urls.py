from django.contrib import admin 
from django.urls import path, include
from restApi import views   

# for Swagger View
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView

#for authentication
from restApi.auth_views import register_user, login_user, logout_user, change_password,forgot_password, reset_password_with_otp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # for Swagger View
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    #for authentication
    path('register/', register_user),
    path('login/', login_user),
    path('logout/', logout_user),
    path('change-password/', change_password),
    path('forgot-password/', forgot_password),
   path('reset-password-otp/', reset_password_with_otp),


    # for employee
    path('employee/',views.employee_list_create, name='emp_list_create'),
    path('employee/<int:pk>',views.employee_retrive_put_delete, name='emp_retrive_put_delete'),
]


