from django.contrib import admin
from django.urls import include, path

# for image files 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('attendance_app.urls')),
   
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)