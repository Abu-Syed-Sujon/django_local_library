# Import required Django modules
from django.db import models
from django.urls import reverse

# For creating unique IDs for BookInstance
import uuid

# For database constraint (case-insensitive unique genre)
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower


# =========================================================
# GENRE MODEL
# =========================================================
class Genre(models.Model):
    """
    Model representing a book genre.
    Example: Science Fiction, Romance, History
    """

    # Genre name field
    name = models.CharField(
        max_length=200,
        unique=True,  # Prevents duplicate genre names
        help_text="Enter a book genre (e.g. Science Fiction)"
    )

    # What will be displayed in Admin panel or shell
    def __str__(self):
        return self.name

    # URL to access detail page of a genre
    def get_absolute_url(self):
        return reverse('genre-detail', args=[str(self.id)])

    class Meta:
        # Ensure genre names are unique ignoring case
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique'
            )
        ]


# =========================================================
# AUTHOR MODEL
# =========================================================
class Author(models.Model):
    """
    Model representing an author.
    """

    # Author first name
    first_name = models.CharField(max_length=100)

    # Author last name
    last_name = models.CharField(max_length=100)

    # Optional birth date
    date_of_birth = models.DateField(null=True, blank=True)

    # Optional death date
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        # Default ordering when querying authors
        ordering = ['last_name', 'first_name']

    # URL for author detail page
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    # How author will appear in admin
    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


# =========================================================
# BOOK MODEL
# =========================================================
class Book(models.Model):
    """
    Model representing a book (not a specific copy).
    """

    # Book title
    title = models.CharField(max_length=200)
    
    objects = models.Manager() #Though django automatically adds this.

    # Each book has ONE author
    # One author can write MANY books
    author = models.ForeignKey(
        Author,
        on_delete=models.RESTRICT,
        null=True
    )

    # Short description of book
    summary = models.TextField(
        max_length=1000,
        help_text="Enter a brief description of the book"
    )

    # Unique ISBN number
    isbn = models.CharField(
        'ISBN',
        max_length=13,
        unique=True,
        help_text="13 Character ISBN number"
    )

    # Book can have multiple genres
    genre = models.ManyToManyField(
        Genre,
        help_text="Select genre for this book"
    )

    # How the book will appear in admin
    def __str__(self):
        return self.title

    # URL to access book detail page
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


# =========================================================
# BOOK INSTANCE MODEL
# =========================================================
class BookInstance(models.Model):
    """
    Model representing a specific physical copy of a book.
    Example:
    Book: Harry Potter
    Copy 1
    Copy 2
    Copy 3
    """

    # Unique ID for each copy
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this particular book copy"
    )

    # Which book this copy belongs to
    book = models.ForeignKey(
        Book,
        on_delete=models.RESTRICT,
        null=True
    )

    # Printing/version of the book
    imprint = models.CharField(max_length=200)

    # Date when book should be returned
    due_back = models.DateField(null=True, blank=True)

    # Status choices
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    # Current status of the book
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability'
    )

    class Meta:
        # Sort book instances by due date
        ordering = ['due_back']

    # How instance will appear in admin
    def __str__(self):
        return f"{self.id} ({self.book.title})"