from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_app(request):
    return redirect('/app/')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("app/", include("tracker.urls")),
    path("", redirect_to_app, name="root"),
]


