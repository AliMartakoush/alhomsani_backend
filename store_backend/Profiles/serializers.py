'''from rest_framework import serializers
from .models import Profile
from store.models import Product

class ProfileSerializer(serializers.ModelSerializer):
    favorite_cars = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=True
    )

    class Meta:
        model = Profile
        fields = ['user', 'name', 'profile_picture', 'contact_info', 'favorite_cars']
'''
from rest_framework import serializers
from .models import Profile, ActivityLog,Reviews
from store.models import Product  # Importing the Product model for favorites & bookmarks
from cloudinary.exceptions import Error as CloudinaryError
from cloudinary.utils import cloudinary_url
from cloudinary import uploader

class ActivityLogSerializer(serializers.ModelSerializer):
    """Serializer for activity log entries."""
    class Meta:
        model = ActivityLog
        fields = ['profile', 'product', 'action', 'timestamp']
        read_only_fields = ['profiled', 'product', 'timestamp']

from rest_framework import serializers
from cloudinary.uploader import upload as cloudinary_upload, destroy as cloudinary_destroy
from cloudinary.utils import cloudinary_url
from cloudinary.exceptions import Error as CloudinaryError

from .models import Profile, Product, ActivityLog
from .serializers import ActivityLogSerializer  # if not already imported

class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profiles with image, favorites, bookmarks, and activity log."""

    favorite_cars = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Product.objects.all(), required=False
    )
    bookmarked_cars = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Product.objects.all(), required=False
    )
    activity_log = ActivityLogSerializer(many=True, read_only=True, source='activitylog_set')

    profile_picture = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Profile
        fields = [
            'user', 'name', 'location', 'contact_info', 'bio',
            'profile_picture_url', 'favorite_cars', 'bookmarked_cars',
            'activity_log', 'member_since', 'profile_picture'
        ]
        read_only_fields = ['user', 'member_since', 'profile_picture_url']

    def create(self, validated_data):
        image = validated_data.pop('profile_picture', None)
        favorite_cars = validated_data.pop('favorite_cars', [])
        bookmarked_cars = validated_data.pop('bookmarked_cars', [])

        profile_picture_url = None
        profile_picture_public_id = None

        if image:
            try:
                upload_result = cloudinary_upload(image)
                profile_picture_public_id = upload_result.get('public_id')
                profile_picture_url, _ = cloudinary_url(
                    profile_picture_public_id,
                    width=800, height=600, crop="auto", gravity="auto",
                    fetch_format="auto", quality="auto"
                )
            except CloudinaryError as e:
                raise serializers.ValidationError(f"Image upload failed: {str(e)}")

        profile = Profile.objects.create(
            profile_picture_url=profile_picture_url,
            profile_picture_public_id=profile_picture_public_id,
            **validated_data
        )

        if favorite_cars:
            profile.favorite_cars.set(favorite_cars)
        if bookmarked_cars:
            profile.bookmarked_cars.set(bookmarked_cars)

        return profile

    def update(self, instance, validated_data):
        profile_picture = validated_data.pop('profile_picture', None)
        favorite_cars = validated_data.pop('favorite_cars', None)
        bookmarked_cars = validated_data.pop('bookmarked_cars', None)

        if profile_picture:
            # Delete old image if exists
            if instance.profile_picture_public_id:
                try:
                    cloudinary_destroy(instance.profile_picture_public_id)
                except CloudinaryError as e:
                    raise serializers.ValidationError(f"Image deletion failed: {str(e)}")

            # Upload new image
            try:
                upload_result = cloudinary_upload(profile_picture)
                public_id = upload_result.get('public_id')
                url, _ = cloudinary_url(
                    public_id,
                    width=800, height=600, crop="auto", gravity="auto",
                    fetch_format="auto", quality="auto"
                )
                instance.profile_picture_url = url
                instance.profile_picture_public_id = public_id
            except CloudinaryError as e:
                raise serializers.ValidationError(f"Image upload failed: {str(e)}")

        # Update normal fields
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        # Update many-to-many relationships
        if favorite_cars is not None:
            instance.favorite_cars.set(favorite_cars)
        if bookmarked_cars is not None:
            instance.bookmarked_cars.set(bookmarked_cars)

        return instance



class DummyFavoriteSerializer(serializers.Serializer):
    car_id = serializers.IntegerField()


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField()  # Shows reviewer's __str__ representation
    # If you want to show specific profile fields instead:
    # reviewer_username = serializers.CharField(source='reviewer.user.username', read_only=True)
    reviewer_Profile_pic=serializers.CharField(source='reviewer.profile_picture_url',read_only=True)
    class Meta:
        model = Reviews
        fields = ['id', 'reviewer', 'car', 'review', 'time_written','reviewer_Profile_pic']
        read_only_fields = ['reviewer', 'time_written']
    
class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['review']  # Only need 'review' for creation (car will be from URL, reviewer from request)
