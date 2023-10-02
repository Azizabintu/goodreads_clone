from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from api.serializers import BookReviewSerializers
from books.models import Review



'''class BookReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookReviewSerializers
    queryset = Review.objects.all()
    lookup_field = 'id'
    def get(self, request, id):
        book_review = Review.objects.get(id=id)

        json_response = {
            "id": book_review.id,
            "stars_given": book_review.stars_given,
            "comment": book_review.comment,
            "book": {
                "id": book_review.book.id,
                "title": book_review.book.title,
                "description": book_review.book.description,
                "isbn": book_review.book.isbn
            },
            "user":{
                "id": book_review.user.id,
                "username": book_review.user.username,
                "first_name": book_review.user.first_name,
                "last_name": book_review.user.last_name
            }
        }
        serializer = BookReviewSerializers(book_review)

        return Response(data=serializer.data)

    def delete(self, request, id):
        book_review = Review.objects.get(id=id)
        book_review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id):
        book_review = Review.objects.get(id=id)
        seralizer = BookReviewSerializers(instance=book_review, data=request.data)

        if seralizer.is_valid():
            seralizer.save()
            return Response(data=seralizer.data,status=status.HTTP_200_OK)

        return Response(data=seralizer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        book_review = Review.objects.get(id=id)
        seralizer = BookReviewSerializers(instance=book_review, data=request.data, partial=True)

        if seralizer.is_valid():
            seralizer.save()
            return Response(data=seralizer.data,status=status.HTTP_200_OK)

        return Response(data=seralizer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookReviewListAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookReviewSerializers
    queryset = Review.objects.all().order_by("-created_ad")
    def get(self, request):
        book_reviews = Review.objects.all().order_by("-created_ad")
        paginator = PageNumberPagination()
        page_obj = paginator.paginate_queryset(book_reviews,request)
        serializer = BookReviewSerializers(page_obj, many=True)
        return Response(data=serializer.data)
        return paginator.get_paginated_response(serializer.data)
    def post(self,request):
        serializer = BookReviewSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''
class BookReviewsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BookReviewSerializers
    queryset = Review.objects.all().order_by("-created_ad")
    lookup_field = 'id'