
from django.test import TestCase
from django.urls import reverse
from books.models import Book,Author,Book_Author,Review
from users.models import CustomUser


# Create your tests here.

class BookTestCases(TestCase):
    def test_no_book(self):
        response = self.client.get(reverse('books:list'))

        self.assertContains(response, 'No books found')

    def test_books_list(self):
        book1 = Book.objects.create(title='Book1', description='description1', isbn= '12345')
        book2 = Book.objects.create(title='Book2', description='description2', isbn='12341')
        book3 = Book.objects.create(title='Book3', description='description3', isbn='12342')
        book4 = Book.objects.create(title='Book4', description='description3', isbn='12343')
        book5 = Book.objects.create(title='Book5', description='description5', isbn='12344')

        response = self.client.get(reverse('books:list')+'?page_size=2')
        for book in [book1, book2]:
            self.assertContains(response, book.title)


        response = self.client.get(reverse('books:list') + "?page=2&?page_size=2")
        for book in [book3, book4]:
            self.assertContains(response, book.title)

        response = self.client.get(reverse('books:list') + "?page=3&?page_size=2")
        for book in [book5]:
            self.assertContains(response, book.title)

    def test_detail_page(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='12345')

        response = self.client.get(reverse('books:detail', kwargs={'id': book.id}))

        self.assertContains(response, book.title)

        self.assertContains(response, book.description)

    def test_search(self):
        book1 = Book.objects.create(title='Sport', description='description1', isbn='12345')
        book2 = Book.objects.create(title='Sevgi va sadoqat', description='description2', isbn='12341')
        book3 = Book.objects.create(title='Izabilniy ayol', description='description3', isbn='12342')

        response = self.client.get(reverse('books:list') + "?q=Sport")
        self.assertContains(response,book1.title)
        self.assertNotContains(response,book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list') + "?q=sevgi")
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book3.title)
        self.assertNotContains(response, book1.title)

        response = self.client.get(reverse('books:list') + "?q=ayol")
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)

class  BookReviewTestCase(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='12345')

        db_user = CustomUser.objects.create(
        username='aziza', first_name='Aziza', last_name='Babashova',
            email='aziza.babashova@mail.ru')
        db_user.set_password('12345')
        db_user.save()
        self.client.login(username='aziza', password='12345')

        self.client.post(reverse("books:reviews",kwargs={"id":book.id}), data={
            "stars_given": 3,
            "comment":"Nice book"
        })
        book_reviews=book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, "Nice book")
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, db_user)

    def test_add_wrong_stars(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='12345')

        db_user = CustomUser.objects.create_user(
            username='aziza', first_name='Aziza', last_name='Babashova',
            email='aziza.babashova@mail.ru')
        db_user.set_password('12345')
        db_user.save()
        self.client.login(username='aziza', password='12345')

        response = self.client.post(reverse("books:reviews", kwargs={"id": book.id}), data={
            "stars_given": 6,
            "comment": "Nice book"
        })
        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 0)


    def test_login_required(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='12345')

        response = self.client.get(reverse("books:reviews", kwargs={"id": book.id}))

        self.assertEqual(response.url, '/users/login/' + '?next=/books/' + str(book.id)+'/reviews/')
        self.assertEqual(response.status_code, 302)

    def test_author_contain_page(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='12345')
        author = Author.objects.create(first_name = "Aziza", last_name = "Babashova", email="aziza.babashova@mail.ru",bio="born 1996")
        book_author =Book_Author.objects.create(book = book, author= author)


        response = self.client.get(reverse('books:detail', kwargs={'id': book.id}))

        self.assertContains(response, book.title)

        self.assertContains(response, book.description)

        self.assertContains(response, author.first_name)

        self.assertContains(response, author.last_name)

    def test_book_review_edit(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='12345')
        db_user = CustomUser.objects.create_user(
            username='aziza', first_name='Aziza', last_name='Babashova',
            email='aziza.babashova@mail.ru')
        db_user.set_password('12345')
        db_user.save()
        self.client.login(username='aziza', password='12345')
        review = Review.objects.create(user=db_user, book=book, comment="this is nice book.", stars_given=3)
        response = self.client.post(
            reverse("books:review_edit" ,kwargs={'book_id': book.id, 'review_id': book.bookreview_set.get(stars_given=3).id}),
            data={
                "stars_given": 4,
                "comment": 'It is a bit boring book',
            }

        )

        review1 = Review.objects.get(pk=review.pk)

        self.assertEqual(review1.comment, 'It is a bit boring book')
        self.assertEqual(review1.stars_given, 4)

    def test_confirm_delete_review(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='12345')
        db_user = CustomUser.objects.create_user(
            username='aziza', first_name='Aziza', last_name='Babashova',
            email='aziza.babashova@mail.ru')
        db_user.set_password('12345')
        db_user.save()
        self.client.login(username='aziza', password='12345')
        review = Review.objects.create(user=db_user, book=book, comment="this is nice book.", stars_given=3)

        response = self.client.get(
            reverse("books:review_delete_confirm",
                    kwargs={'book_id': book.id, 'review_id': book.bookreview_set.get(stars_given=3).id})
        )
        book_reviews = book.bookreview_set.all()
        self.assertEqual(book_reviews.count(), 1)
        self.assertContains(response,"Are you sure to delete this comment")

    def test_delete_review(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='12345')
        db_user = CustomUser.objects.create_user(
            username='aziza', first_name='Aziza', last_name='Babashova',
            email='aziza.babashova@mail.ru')
        db_user.set_password('12345')
        db_user.save()
        self.client.login(username='aziza', password='12345')
        review = Review.objects.create(user=db_user, book=book, comment="this is nice book.", stars_given=3)
        id = book.bookreview_set.all()[0].id
        response = self.client.get(
            reverse("books:review_delete",
                    kwargs={'book_id': book.id, 'review_id': id })
        )
        book.refresh_from_db
        book_reviews = book.bookreview_set.all()
        self.assertEqual(book_reviews.count(), 0)
