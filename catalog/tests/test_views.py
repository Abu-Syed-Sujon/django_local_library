from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from catalog.models import Author, Book
from django.contrib.auth.models import Permission


class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()

        # test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        # author (match your real model)
        self.author = Author.objects.create(
            first_name="John",
            last_name="Doe",
            date_of_birth="1990-01-01",
            date_of_death="2000-01-01"
        )

        # book (adjust if your Book model differs)
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author
        )

    # -------------------------
    # HOME PAGE TEST
    # -------------------------
    def test_index_view(self):
        response = self.client.get(reverse('catalog:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/index.html")

    # -------------------------
    # BOOK LIST VIEW
    # -------------------------
    def test_book_list_view(self):
        response = self.client.get(reverse('catalog:books'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")

    # -------------------------
    # BOOK DETAIL VIEW
    # -------------------------
    def test_book_detail_view(self):
        response = self.client.get(
            reverse('catalog:book-detail', args=[self.book.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)

    # -------------------------
    # LOGIN REQUIRED VIEW (redirect check)
    # -------------------------
    def test_borrowed_books_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('catalog:all-borrowed'))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login'))

    # -------------------------
    # LOGIN REQUIRED VIEW (logged in)
    # -------------------------
    def test_borrowed_books_logged_in(self):
        self.client.login(username="testuser", password="testpass123")
        
        # ADD REQUIRED PERMISSION
        permission = Permission.objects.get(codename='can_mark_returned')
        self.user.user_permissions.add(permission)
        
        response = self.client.get(reverse('catalog:all-borrowed'))

        self.assertEqual(response.status_code, 200)