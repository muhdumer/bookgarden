from django.urls import path 
from .views import BookListView,SingleBookView,SearchListView

app_name="product_app"

urlpatterns = [
    path('<int:pk>/',BookListView.as_view(),name="category_product_list"),
    path('',BookListView.as_view(),name="product_list"),
    path('single/<int:pk>/<str:bookname>/',SingleBookView.as_view(),name="single_book"),
    path('searchtab/',SearchListView.as_view(),name='search_list_of_books')
]
