from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from books.models import Book, Review, CustomUser


class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username='aziza')
        self.db_user.set_password('12345')
        self.db_user.save()
        self.client.login(username='aziza',password='12345')

    def test_book_review_detail(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='12345')
        review = Review.objects.create(user=self.db_user, book=book, comment="this is nice book.", stars_given=3)

        response = self.client.get(
            reverse("api:review-detail",
                    kwargs={'id': review.id})
        )

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data['id'],review.id)
        self.assertEqual(response.data['stars_given'],3)
        self.assertEqual(response.data['comment'], review.comment)
        self.assertEqual(response.data['book']['id'], review.book.id)
        self.assertEqual(response.data['book']['title'], 'Book1')
        self.assertEqual(response.data['book']['description'], 'description1')
        self.assertEqual(response.data['book']['isbn'], '12345')
        self.assertEqual(response.data['user']['id'],review.user.id)
        self.assertEqual(response.data['user']['username'], 'aziza')

    def test_review_list_detail(self):
        db_user2=CustomUser.objects.create_user(username='Mustafa', first_name='Uktam')
        book = Book.objects.create(title='Book1', description='description1', isbn='12345')
        review1 = Review.objects.create(user=db_user2, book=book, comment="this is nice book.", stars_given=3)
        review2 = Review.objects.create(user=self.db_user, book=book, comment="this is boring book.", stars_given=4)
        response = self.client.get(reverse("api:review-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']),2)
        self.assertEqual(response.data['count'],2)
        self.assertIn('next',response.data)
        self.assertIn('previous',response.data)


        self.assertEqual(response.data['results'][0]['id'], review2.id)
        self.assertEqual(response.data['results'][0]['stars_given'],4)
        self.assertEqual(response.data['results'][0]['comment'], "this is boring book.")
        self.assertEqual(response.data['results'][1]['id'], review1.id)
        self.assertEqual(response.data['results'][1]['stars_given'], 3)
        self.assertEqual(response.data['results'][1]['comment'], "this is nice book.")

    def test_review_delete(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='12345')
        review = Review.objects.create(user=self.db_user, book=book, comment="this is nice book.", stars_given=3)

        response = self.client.delete(
            reverse("api:review-detail",
                    kwargs={'id': review.id})
        )
        self.assertEqual(response.status_code, 204)

        book_reviews=book.bookreview_set.all()
        count = book_reviews.count()
        self.assertEqual(count, 0)
        self.assertFalse(Review.objects.filter(id=review.id).exists())

    def test_review_patch(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='12345')
        review = Review.objects.create(user=self.db_user, book=book, comment="this is nice book.", stars_given=3)

        response = self.client.patch(reverse("api:review-detail",kwargs={'id': review.id}),data={"stars_given":5})
        review.refresh_from_db()

        self.assertEqual(review.stars_given, 5)
        self.assertEqual(response.status_code, 200)

    def test_review_put(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='12345')
        review = Review.objects.create(user=self.db_user, book=book, comment="this is nice book.", stars_given=3)

        response = self.client.put(reverse("api:review-detail",kwargs={'id': review.id}),data={"stars_given":5,"comment":"Zo'r kitob ekan","user_id":self.db_user.id,"book_id":book.id})
        review.refresh_from_db()

        self.assertEqual(review.stars_given, 5)
        self.assertEqual(review.comment, "Zo'r kitob ekan")
        self.assertEqual(response.status_code, 200)
    def test_review_post(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='12345')
        response = self.client.post(reverse("api:review-list"),
                                   data={"stars_given": 5, "comment": "Zo'r kitob ekan", "user_id": self.db_user.id,
                                         "book_id": book.id})

        self.assertEqual(response.status_code, 201)
        review=Review.objects.get(book=book)
        self.assertEqual(review.stars_given, 5)
        self.assertEqual(review.comment, "Zo'r kitob ekan")
