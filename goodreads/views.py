from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from books.models import Review

def landing_page(request):
    #print(request.COOKIES['sessionid'])

    #print(request.user.is_authenticated)
    return render(request, "landing.html")


def reviews_page(request):
    reviews = Review.objects.all().order_by("-created_ad")
    page_size = request.GET.get("page_size",2)
    paginator = Paginator(reviews,page_size)
    page_num = request.GET.get('page',1)
    page_obj = paginator.get_page(page_num)
    return render(request, "reviews.html" ,{"page_obj": page_obj})