from django.db import models

# Create your models here.
class reader(models.Model):
    def __str__(self):
        return self.reader_name
    reference_id = models.CharField(max_length=200)
    reader_name = models.CharField(max_length=200)
    reader_contact = models.IntegerField(max_length=200)
    reader_address = models.TextField()
    active=models.BooleanField(default=True)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    category = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)
    quantity = models.PositiveIntegerField(default=1)
    available = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

class BookIssue(models.Model):

    reader = models.ForeignKey(
        reader,
        on_delete=models.CASCADE
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    issue_date = models.DateField(
        auto_now_add=True
    )

    due_date = models.DateField()

    returned = models.BooleanField(
        default=False
    )

    return_date = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.reader.reader_name} - {self.book.title}"
