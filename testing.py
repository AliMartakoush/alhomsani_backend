from django.urls import path ,include
from django.conf.urls import handler400, handler403,handler404,handler500
from . import error_handler

urlpatterns=[
    path("home/mockpath/",include('mockApp.urls',namespace="mockApp"))
]

handler500='error_handler.custom_500'
handler403='error_handler.custom_403'
handler400='error_handler.custom_400'
handler404='error_handler.custom_404'

#error handler  has 4 funcrions with the form 
#def custom_500(request):
    #json= {"message":<string>,"status":<int>}
    #return json