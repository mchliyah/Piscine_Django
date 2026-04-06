from django.http import HttpResponse
from django.urls import path


def hello_world(_request):
    return HttpResponse("Hello World !")


urlpatterns = [
    path("helloworld", hello_world),
]