from django.urls import path
from .views import ProductDetail,ProductList,FilteredProductListView
from django.conf import settings
from django.conf.urls.static import static
from Profiles.views import ReviewListView,CreateReviewView
app_name='store_post'
urlpatterns=[
    path('<int:pk>/',ProductDetail.as_view(),name='detailcreate'),
    path('',ProductList.as_view(),name='listcreate'), 
    path('filtered/',FilteredProductListView.as_view(),name='filtered_view'),
    path('<int:car_id>/reviews/', ReviewListView.as_view(), name='car-reviews'),
    path('<int:car_id>/reviews/create/', CreateReviewView.as_view(), name='create-review'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
