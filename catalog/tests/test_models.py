from django.test import TestCase
from django.urls import reverse
from catalog.models import Author


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author = Author.objects.first()
        self.assertEqual(author._meta.get_field('first_name').verbose_name, 'first name')

    def test_last_name_label(self):
        author = Author.objects.first()
        self.assertEqual(author._meta.get_field('last_name').verbose_name, 'last name')

   # def test_date_of_birth_label(self):
    #    author = Author.objects.first()
    #    self.assertEqual(author._meta.get_field('date_of_birth').verbose_name, 'date of birth')
    
    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        self.assertEqual(author._meta.get_field('date_of_birth').verbose_name, 'born')


    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        self.assertEqual(author._meta.get_field('date_of_death').verbose_name, 'died')
    

    def test_first_name_max_length(self):
        author = Author.objects.first()
        self.assertEqual(author._meta.get_field('first_name').max_length, 100)

    def test_last_name_max_length(self):
        author = Author.objects.first()
        self.assertEqual(author._meta.get_field('last_name').max_length, 100)

    def test_object_name(self):
        author = Author.objects.first()
        expected = f'{author.last_name}, {author.first_name}'
        self.assertEqual(str(author), expected)

    def test_get_absolute_url(self):
        author = Author.objects.first()
        self.assertEqual(author.get_absolute_url(), reverse('catalog:author-detail', args=[author.id]))

    def test_date_of_birth_null(self):
        author = Author.objects.first()
        self.assertIsNone(author.date_of_birth)

    def test_date_of_death_null(self):
        author = Author.objects.first()
        self.assertIsNone(author.date_of_death)

    def test_date_of_birth_blank(self):
        author = Author.objects.first()
        self.assertTrue(author._meta.get_field('date_of_birth').blank)

    def test_date_of_death_blank(self):
        author = Author.objects.first()
        self.assertTrue(author._meta.get_field('date_of_death').blank)