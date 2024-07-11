from django.urls import path


from photo.views import (
        login,
        home,
        upload,
        oss_home, 
        fetch_photos,
    )
from django.urls import path
from . import views

from django.views.generic import TemplateView

from django.urls import path
from . import views


app_name = 'photo'

urlpatterns = [

    path('', home, name='home'),
    path('upload/', upload, name='upload'),

    path('oss-home/', oss_home, name='oss_home'),
    path('delete_photo/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('endless-home/',TemplateView.as_view(template_name='photo/endless_list.html'),name='endless_home'
    ),
    path('fetch/', fetch_photos, name='fetch'),
]
