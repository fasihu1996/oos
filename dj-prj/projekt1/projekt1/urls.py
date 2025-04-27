"""
URL configuration for projekt1 project.

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
from book.models import Category
from book.views import get_book_list, author_details, get_author_list
from django.contrib import admin
from django.urls import path
from django.views.generic import ListView
from uhrzeit.views import get_time

urlpatterns = [
    path('uhrzeit/', get_time),
    path('', get_time),
    path('uhrzeit/<str:continent>/<str:city>', get_time),
    path('books/', get_book_list, name="book_list"),
    path('authors/', get_author_list, name="author_list"),
    path('author/add/', author_details, name="add_author"),
    path('author/edit/<int:pk>', author_details, name="edit_author"),

    path('categories/', ListView.as_view(model=Category,
                                         extra_context={"page_title": "KatListe", })),
    path('admin/', admin.site.urls),
]
