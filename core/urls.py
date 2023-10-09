# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from ckeditor_uploader import views as ckeditor_views

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register



    # ADD NEW Routes HERE
    path('clients/', include("clients.urls")),
    path('products/',include("products.urls")),
    path('factures/', include('factures.urls')),
    path('payment/', include('payment.urls')),    
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # Leave `Home.Urls` as last the last line
    path("", include("apps.home.urls")),
]


