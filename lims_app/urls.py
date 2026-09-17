from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path("save_student/", views.save_student, name="save_student"),
    path("readers/", views.readers_tab, name="readers"),
    path("readers/add", views.save_readers, name="save_readers"),
    path('books/', views.books, name='books'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path("my-bag/", views.my_bag, name="my_bag"),
    path("add_to_bag/<int:book_id>/",views.add_to_bag,name="add_to_bag"),
    path( "remove_from_bag/<int:book_id>/",views.remove_from_bag,name="remove_from_bag"),
    path("returns/", views.return_books, name="return_books"),
    path("return-book/<int:issue_id>/",views.return_book,name="return_book"),
]