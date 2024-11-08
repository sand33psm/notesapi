from django.contrib import admin
from django.urls import path, include
from django.urls import re_path, path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    re_path(r'^(?!api/).*$', TemplateView.as_view(template_name="index.html")),

]
