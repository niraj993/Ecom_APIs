 
from django.contrib import admin
from django.urls import path,include
from .views import index
from configs.endpoints import AUTH,BASE_ENDPOINT

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",index,name="home"),
    path(BASE_ENDPOINT + AUTH,include("accounts.urls")),
]
