from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from django.urls import path, re_path
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from drf_spectacular.views import SpectacularSwaggerView,SpectacularAPIView


schema_view = get_schema_view(
   openapi.Info(
      title="Alhomsani API",
      default_version='v1',
      description="Car marketplace API",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls', namespace='store')),
    path('api/', include('store_api.urls', namespace='store_api')),
    #path('api/users/', include('users.urls', namespace='users')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('profiles/',include('Profiles.urls',namespace='profiles')),
    path('schema/',SpectacularAPIView.as_view(),name='schema'),
    path('schema/docs/',SpectacularSwaggerView.as_view(url_name='schema'),name='docs'),
    path('payment/',include('payment.urls',namespace='payment')),

]

