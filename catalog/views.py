from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def index(request):
    """Home Page View"""
    #Total Books
    num_books = Book.objects.count() # pylint: disable=no-member
    # Total Copies
    num_instances = BookInstance.objects.count() # pylint: disable=no-member
    #Available Copies
    num_instances_available = BookInstance.objects.filter(status='a').count() # pylint: disable=no-member
    # Total Authors
    num_authors = Author.objects.count() # pylint: disable=no-member
    
    # Session Part
    # Get Visit Count
    num_visits= request.session.get('num_visits', 0)
    
        # Increase visit count
    num_visits += 1

    # Save it back to session
    request.session['num_visits'] = num_visits
    
    
    context = {
       "num_books" : num_books,
        "num_instances":num_instances,
        "num_instances_available": num_instances_available,
    
        "num_authors": num_authors,
    }
    
    return render(request, "catalog/index.html", context)

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
    

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    View to show books borrowed by the currently logged-in user.
    
    LoginRequiredMixin:
        - Prevents anonymous users from accessing this page
        - Redirects to login page if not authenticated
    """

    model = BookInstance  # Model to query
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10  # Optional: limits results per page

    def get_queryset(self):
        """
        Override default queryset:
        - Only show books borrowed by current user
        - Only show books with status 'o' (on loan)
        - Order by due date
        """
        return BookInstance.objects.filter(
            borrower=self.request.user,
            status='o'
        ).order_by('due_back')
        
from django.contrib.auth.decorators import login_required, permission_required

@login_required  # Must be logged in
@permission_required('catalog.can_mark_returned', raise_exception=True)
def my_view(request):
    """
    Only users with 'can_mark_returned' permission can access.
    
    raise_exception=True:
        - Returns 403 instead of redirect
    """
    pass
