from django.test import TestCase
from catalog.forms import AuthorForm, RenewBookModelForm
from catalog.models import Author
import datetime


class FormTests(TestCase):

    def setUp(self):
        self.author = Author.objects.create(
            first_name="John",
            last_name="Doe",
            date_of_birth="1990-01-01",
            date_of_death="2000-01-01"
        )

    # -------------------------
    # AUTHOR FORM TEST
    # -------------------------
    def test_author_form_valid_data(self):
        form = AuthorForm(data={
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "date_of_death": ""
        })

        self.assertTrue(form.is_valid())

    def test_author_form_missing_data(self):
        form = AuthorForm(data={})

        self.assertFalse(form.is_valid())

    # -------------------------
    # RENEW BOOK FORM TEST
    # -------------------------
    def test_renew_book_form_valid_date(self):
        future_date = datetime.date.today() + datetime.timedelta(days=7)

        form = RenewBookModelForm(data={
            "due_back": future_date
        })

        self.assertTrue(form.is_valid())

    def test_renew_book_form_past_date(self):
        past_date = datetime.date.today() - datetime.timedelta(days=1)

        form = RenewBookModelForm(data={
            "due_back": past_date
        })

        self.assertFalse(form.is_valid())