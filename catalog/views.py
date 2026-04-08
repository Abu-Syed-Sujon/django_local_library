from urllib import request
import datetime
from django import forms
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import RenewBookModelForm, AuthorForm

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
    """
    View to display detailed information about a specific book.
    """
    model = Book


class AuthorListView(generic.ListView):
    """
    View to display a list of all authors.
    """
    model = Author
    ordering = ['last_name']
  


class AuthorDetailView(generic.DetailView):
    """
    View to display detailed information about a specific author.
    """
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
        



@login_required  # Must be logged in
@permission_required('catalog.can_mark_returned', raise_exception=True)
def mark_returned_view(request, pk):
    """
    View to mark a book instance as returned.
    
    Permissions:
        - User must be logged in
        - User must have 'can_mark_returned' permission
        - Returns 403 if user lacks permission
    """
    book_instance = get_object_or_404(BookInstance, pk=pk)
    
    # mark the book as returned
    book_instance.status = 'a'  # Set status to 'available'
    book_instance.save()  # Save changes to database
    return redirect('catalog:all-borrowed')  # Redirect to list of all borrowed books

class AllBorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    """
    View to display all borrowed books for staff with appropriate permissions.
    
    PermissionRequiredMixin:
        - Requires 'catalog.can_mark_returned' permission
        - Returns 403 if user lacks permission
    """
    model = BookInstance
    template_name = 'catalog/all_borrowed_books.html'
    context_object_name = 'bookinstance_list'
    permission_required = 'catalog.can_mark_returned'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').select_related('book', 'borrower').order_by('due_back')  # pylint: disable=no-member\class 'BookInstance'
    
@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """
    View for librarians to renew a book instance.
    Requires 'can_mark_returned' permission.
    """
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookModelForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()
            return redirect('catalog:all-borrowed')
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

    return render(request, 'catalog/book_renew_librarian.html', {
        'form': form,
        'book_instance': book_instance
    })
    

    
    
class AuthorCreate(PermissionRequiredMixin, generic.CreateView):  # pylint: disable=too-many-ancestors
    """Create a new author. Requires appropriate permissions."""
    model = Author
    form_class = AuthorForm
    permission_required = 'catalog.add_author'

class AuthorUpdate(PermissionRequiredMixin, generic.UpdateView):  # pylint: disable=too-many-ancestors
    """Update an existing author. Requires appropriate permissions."""
    model = Author
    form_class = AuthorForm
    permission_required = 'catalog.change_author'

class AuthorDelete(PermissionRequiredMixin, generic.DeleteView):  # pylint: disable=too-many-ancestors
    """Delete an author. Requires appropriate staff permissions."""
    model = Author
    #success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'
    
    def get_success_url(self):
        return reverse_lazy('catalog:authors')