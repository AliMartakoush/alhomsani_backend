from django.shortcuts import render
from rest_framework import generics
from store.models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticatedOrReadOnly,DjangoModelPermissions,IsAuthenticated
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly,BasePermission,SAFE_METHODS
from drf_spectacular.utils import extend_schema,OpenApiParameter
from cloudinary.uploader import destroy as cloudinary_destroy
from cloudinary.exceptions import Error as CloudinaryError
      
      

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Delete image from Cloudinary if it exists
        if instance.image_public_id:
            try:
                cloudinary_destroy(instance.image_public_id)
            except CloudinaryError as e:
                return Response(
                    {"detail": f"Failed to delete image from Cloudinary: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # Delete the DB object
        return super().destroy(request, *args, **kwargs) 

   

class ProductList(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Product.objects.filter(availability='in_stock')
    serializer_class=ProductSerializer 


@extend_schema(
    parameters=[
        OpenApiParameter(name='car_type', description='Search car by type', required=False, type=str),
    ]
)
class FilteredProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        car_type = self.request.query_params.get('car_type')
        if car_type:
            return Product.objects.filter(car_type=car_type)
        return Product.objects.all()