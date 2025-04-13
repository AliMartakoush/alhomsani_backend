from django.urls import path
from .views import ProductDetail,ProductList,FilteredProductListView
from django.conf import settings
from django.conf.urls.static import static
app_name='store_post'
urlpatterns=[
    path('<int:pk>/',ProductDetail.as_view(),name='detailcreate'),
    path('',ProductList.as_view(),name='listcreate'), 
    path('filtered/',FilteredProductListView.as_view(),name='filtered_view') 



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
