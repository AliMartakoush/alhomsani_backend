from django.urls import path, include
from .views import AddToFavoritesView,AddToBookmarksView,RemoveFromBookmarksView,RemoveFromFavoritesView
from .views import ActivityLogListView,ActivityLogPagination,UserProfileView
from .views import ReviewListView,CreateReviewView

app_name='Profiles'

urlpatterns=[
    path('',UserProfileView.as_view(),name='Profile_View'),
    path('favorites/add/<int:product_id>/',AddToFavoritesView.as_view(),name='add_to_favorites'),
    path('favorites/remove/<int:product_id>/',RemoveFromFavoritesView.as_view(),name='remove_from_favorites'),
    path('bookmarks/add/<int:product_id>/',AddToBookmarksView.as_view(),name='add_to_bookmarks'),
    path('bookmarks/remove/<int:product_id>/',RemoveFromBookmarksView.as_view(),name='remove_from_bookmarks'),
    path('activity/',ActivityLogListView.as_view(),name='activity_log_view'),
]