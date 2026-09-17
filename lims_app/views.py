from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *

def home(request):
    return render(request, "home.html",context={"current_tab": "home"})

def readers(request):
    return render(request, "readers.html",context={"current_tab": "readers"})

def save_student(request):
    if request.method == "POST":
        student_name = request.POST.get("student_name")

        return render(request, "library.html", {
            "student_name": student_name
        })

    return render(request, "index.html")

def readers_tab (request):
    if request.method == "GET":
        readers = reader.objects.all()
        return render(request, "readers.html",
                  context={"current_tab": "readers",
                           "readers": readers})
    else:
        query = request.POST.get("query")
        readers = reader.objects.raw("select * from lims_app_reader where reader_name like '%"+query+"%'")
        return render(request, "readers.html",
                  context={"current_tab": "readers",
                           "readers": readers})

def save_readers(request):
    if request.method == "POST":
        reader_item = reader(
                  reference_id=request.POST.get("reader_ref_id"),
                  reader_name=request.POST.get("reader_name"),
                  reader_contact=request.POST.get("reader_contact"),
                  reader_address=request.POST.get("reader_address"),
                  active=True
                )
    reader_item.save()
    return redirect('/readers')


def books(request):
    query = request.GET.get("q", "")

    if query:
        book_list = Book.objects.filter(title__icontains=query)
    else:
        book_list = Book.objects.all()

    return render(request, "books.html", {
        "books": book_list,
        "query": query
    })


def add_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        category = request.POST.get("category")
        isbn = request.POST.get("isbn")
        quantity = request.POST.get("quantity")
        available = request.POST.get("available")

        Book.objects.create(
            title=title,
            author=author,
            category=category,
            isbn=isbn,
            quantity=quantity,
            available=available
        )

        return redirect("books")

    return render(request, "book_form.html", {
        "form_title": "Add New Book",
        "button_text": "Add Book"
    })


def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.category = request.POST.get("category")
        book.isbn = request.POST.get("isbn")
        book.quantity = request.POST.get("quantity")
        book.available = request.POST.get("available")

        book.save()

        return redirect("books")

    return render(request, "book_form.html", {
        "form_title": "Edit Book",
        "button_text": "Save Changes",
        "book": book
    })


def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        book.delete()

    return redirect("books")

def my_bag(request):
    bag = request.session.get("my_bag", [])

    books = Book.objects.filter(id__in=bag)

    available_count = books.filter(available__gt=0).count()

    return render(request, "my_bag.html", {
        "books": books,
        "available_count": available_count
    })


def add_to_bag(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    bag = request.session.get("my_bag", [])


    if book_id not in bag:
        bag.append(book_id)

    request.session["my_bag"] = bag
    request.session.modified = True

    return redirect("my_bag")


def remove_from_bag(request, book_id):
    bag = request.session.get("my_bag", [])

    if book_id in bag:
        bag.remove(book_id)

    request.session["my_bag"] = bag
    request.session.modified = True

    return redirect("my_bag")

def return_books(request):

    issues = BookIssue.objects.select_related(
        "reader",
        "book"
    ).filter(
        returned=False
    )

    query = request.GET.get("q", "")

    if query:
        issues = issues.filter(
            reader__reader_name__icontains=query
        )

    return render(request, "return.html", {
        "issues": issues,
        "query": query,
        "today": timezone.now().date()
    })


def return_book(request, issue_id):

    issue = get_object_or_404(
        BookIssue,
        id=issue_id
    )

    if request.method == "POST":

        issue.returned = True
        issue.return_date = timezone.now().date()
        issue.save()

        issue.book.available += 1

        if issue.book.available > issue.book.quantity:
            issue.book.available = issue.book.quantity

        issue.book.save()

    return redirect("return_books")







