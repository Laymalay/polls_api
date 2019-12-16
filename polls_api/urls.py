"""polls_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path
from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView

from polls_api.schema import schema
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('csrf/', views.csrf),
    # path('graphql', GraphQLView.as_view(graphiql=True, schema=schema)),
    url(r'^graphql', FileUploadGraphQLView.as_view(graphiql=True)),
]
