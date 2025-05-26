"""
URL configuration for charity project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/donation/', include('donations.urls')),
    path('api/project_tags/', include('project_tag.urls')),
    path('api/categories/', include('category.urls')),
    path('api/user/', include('user.api.urls')),
    path('api/tag/', include('tag.api.urls')),

    path('api/project-images/', include('project_image.urls')),
    path('api/comments/', include('comments.urls')),
    path('api/project-reports/', include('project_reports.api.urls')),
    path('api/comment-reports/', include('comment_reports.api.urls')),

    path('api/project/',include('project.api.urls')),
    path('api/rate/',include('rate.api.urls')),
]
