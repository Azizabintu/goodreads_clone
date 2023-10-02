from rest_framework import serializers
from books.models import Book, CustomUser, Review


'''class BookSerializers(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    isbn = serializers.CharField(max_length=17)

class UserSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    email = serializers.EmailField(max_length=255)
class BookReviewSerializers(serializers.Serializer):
    stars_given = serializers.IntegerField(min_value=1, max_value=5)
    comment = serializers.CharField()
    book = BookSerializers()
    user = UserSerializers()'''


class BookSerializers(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'isbn')

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name','email')

class BookReviewSerializers(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)
    book = BookSerializers(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    book_id = serializers.IntegerField(write_only=True)

    class Meta:
        model=Review
        fields = ('id', 'stars_given', 'comment', 'book', 'user', "user_id", "book_id")