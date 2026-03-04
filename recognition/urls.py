from django.urls import path
from . import views

app_name = 'recognition'

urlpatterns = [
    # We will leave this empty for now or add a dummy path
    # path('', views.index, name='index'),
    path('upload/', views.upload_image, name='upload_image')
]