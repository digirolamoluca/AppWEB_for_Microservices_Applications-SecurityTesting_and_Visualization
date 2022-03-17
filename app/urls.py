from django.urls import path
from . import views


urlpatterns = [
    path('', views.app),
    #path('customize', views.customize),
    #path('viewmacm', views.viewmacm),
]

