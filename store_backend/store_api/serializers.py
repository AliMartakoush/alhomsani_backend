from rest_framework import serializers
from store.models import Product
from django.conf import settings
import cloudinary.uploader
from cloudinary.exceptions import Error as CloudinaryError
from cloudinary.utils import cloudinary_url


from cloudinary.exceptions import Error as CloudinaryError

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Product
        fields = (
            'id', 
            'category', 
            'name', 
            'description', 
            'price', 
            'stock_quantity',
            'sku', 
            'created_at', 
            'updated_at', 
            'availability', 
            'car_type',
            'image_url', 
            'image_public_id',
            'key_features',
            # New automotive fields
            'engine',
            'power',
            'torque',
            'transmission',
            'acceleration_0_100',
            'top_speed',
            'fuel_economy',
            'dimensions',
            'weight_kg',
            'wheelbase_mm',
            'fuel_tank_capacity',
            'trunk_capacity_liters',
            'image',
        )
        
        read_only_fields = ['image_url', 'image_public_id']

    def create(self, validated_data):
        image = validated_data.pop('image',None)

        try:
            upload_result = cloudinary.uploader.upload(image)
            public_id = upload_result.get("public_id")
            image_url, _ = cloudinary_url(
            public_id,
            width=800,
            height=600,
            crop="auto",
            gravity="auto",
            fetch_format="auto",
            quality="auto"
        )
            
        except CloudinaryError as e:
            raise serializers.ValidationError(f"Image upload failed: {str(e)}")

        return Product.objects.create(image_url=image_url, image_public_id=public_id, **validated_data)

    def update(self, instance, validated_data):
        image = validated_data.pop('image', None)

        if image:
            # delete the old image first
            if instance.image_public_id:
                try:
                    cloudinary.uploader.destroy(instance.image_public_id)
                except CloudinaryError as e:
                    raise serializers.ValidationError(f"Image deletion failed: {str(e)}")

            # upload the new one
            try:
                upload_result = cloudinary.uploader.upload(image)
                instance.image_public_id = upload_result.get("public_id")
                instance.image_url, _ = cloudinary_url(
            instance.image_public_id,
            width=800,
            height=600,
            crop="auto",
            gravity="auto",
            fetch_format="auto",
            quality="auto"
        )
                
            except CloudinaryError as e:
                raise serializers.ValidationError(f"Image upload failed: {str(e)}")

        # update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance






class UserRegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ('email', 'user_name', 'first_name')
        extra_kwargs = {'password': {'write_only': True}}
