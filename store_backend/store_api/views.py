from django.shortcuts import render
from rest_framework import generics
from store.models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticatedOrReadOnly,DjangoModelPermissions,IsAuthenticated
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly,BasePermission,SAFE_METHODS
from drf_spectacular.utils import extend_schema,OpenApiParameter
from cloudinary.uploader import destroy as cloudinary_destroy
from cloudinary.exceptions import Error as CloudinaryError
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache  
      
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        cache.clear()  # Clear cache after update
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.image_public_id:
            try:
                cloudinary_destroy(instance.image_public_id)
            except CloudinaryError as e:
                return Response(
                    {"detail": f"Failed to delete image from Cloudinary: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        cache.clear()  # Clear cache after delete
        return super().destroy(request, *args, **kwargs)

   

@method_decorator(cache_page(60 * 30), name='get')  # Cache GETs for 30 minutes
class ProductList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.filter(availability='in_stock')
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache.clear()  # Clear cache after adding new product
        return response



@extend_schema(
    parameters=[
        OpenApiParameter(name='car_type', description='Search car by type', required=False, type=str),
    ]
)
@method_decorator(cache_page(60 * 30), name='get')  # Cache GETs for 30 minutes
class FilteredProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        car_type = self.request.query_params.get('car_type')
        if car_type:
            return Product.objects.filter(car_type=car_type)
        return Product.objects.all()