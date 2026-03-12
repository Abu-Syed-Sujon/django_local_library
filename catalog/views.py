from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre

# Create your views here.

def index(request):
    """Home Page View"""
    num_books = Book.objects.count() # pylint: disable=no-member
    
    num_instances = BookInstance.objects.count() # pylint: disable=no-member
    num_instances_available = BookInstance.objects.filter(status='a').count() # pylint: disable=no-member
    
    num_authors = Author.objects.count() # pylint: disable=no-member
    
    context = {
       "num_books" : num_books,
        "num_instances":num_instances,
        "num_instances_available": num_instances_available,
    
        "num_authors": num_authors,
    }
    
    return render(request, "index.html", context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    

    
class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    ordering = ['last_name']


class AuthorDetailView(generic.DetailView):
    model = Author