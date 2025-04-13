from django.shortcuts import render
from django.shortcuts import HttpResponse




def test(request):
    return HttpResponse("test")




def home(request):
    return render(request,'store/index.html')
