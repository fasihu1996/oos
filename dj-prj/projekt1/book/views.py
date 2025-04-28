from book.forms import *
from book.models import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy


# Create your views here.
#
# class CategoryListView(ListView):
#     model = Category
#     page_title = "Kategorienliste"
#     # hier muss nicht mal mehr das template angegeben werden


def get_book_list(request):
    books = Book.objects.all().order_by("title")

    return render(request, "book/book_list.html", {"page_title": "Meine Bücher",
                                                   "books": books})


def get_author_list(request):
    authors = Author.objects.all().order_by("ln", "fn")

    return render(request, "book/author_list.html", {"page_title": "Autoren",
                                                     "authors": authors})


def author_details(request, pk=None):
    if pk:
        author = Author.objects.get(pk=pk)
    else:
        author = Author()

    if request.method == "POST":
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            messages.success(request, "Author saved")
            return HttpResponseRedirect(reverse_lazy('author_list'))
        else:
            messages.error(request, "The form data is incorrect.")
    else:

        form = AuthorForm(instance=author)

    return render(request, "book/author_details.html", {"page_title": "Author hinzufügen",
                                                        "form": form})
