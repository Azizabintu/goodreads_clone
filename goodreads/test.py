from django.test import TestCase

from django.urls import reverse

from books.models import Book, Review
from users.models import CustomUser

class ReviewTest(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title='Sport', description='description1', isbn='12345')
        db_user = CustomUser.objects.create(
            username='aziza', first_name='Aziza', last_name='Babashova',
            email='aziza.babashova@mail.ru')
        db_user.set_password('12345')
        db_user.save()
        self.client.login(username='aziza', password='12345')

        review1 = Review.objects.create(stars_given=3, comment='comment1', book=book, user=db_user)
        review2 = Review.objects.create(stars_given=4, comment='comment2', book=book, user=db_user)
        review3 = Review.objects.create(stars_given=5, comment='comment3', book=book, user=db_user)

        response = self.client.get(reverse("reviews") + "?page_size=2")

        self.assertNotContains(response, review1.comment)
        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)




