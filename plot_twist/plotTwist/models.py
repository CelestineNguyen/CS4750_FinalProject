from django.db import models

# Create your models here.
class BookDetails(models.Model):
    book_id = models.IntegerField(primary_key=True)
    title = models.TextField()
    isbn = models.TextField()
    pages = models.IntegerField(null=True)
    date_published = models.DateField(null=True)
    description = models.TextField(null=True)
    average_rating = models.FloatField(null=True)
    authors = models.TextField

    class Meta:
        db_table = 'book_details'
        managed = False #view, not a table