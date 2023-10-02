from django.urls import path
from books.views import BookListView, BookDetailView,AddReviewView,BookReviewEdit,ConfirmDeleteReviewView, DeleteReviewView

app_name = 'books'
urlpatterns = [
    path('',BookListView.as_view(), name='list'),
    path('<int:id>/',BookDetailView.as_view(),name='detail'),
    path('<int:id>/reviews/',AddReviewView.as_view(),name='reviews'),
    path('<int:book_id>/reviews/<int:review_id>/edit',BookReviewEdit.as_view(),name='review_edit'),
    path('<int:book_id>/reviews/<int:review_id>/delete/review',ConfirmDeleteReviewView.as_view(),name='review_delete_confirm'),
    path('<int:book_id>/reviews/<int:review_id>/delete',DeleteReviewView.as_view(),name='review_delete'),
]