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
    authors = models.TextField()

    class Meta:
        db_table = 'book_details'
        managed = False  # view, not a table


class ListBooks(models.Model):
    pk = models.CompositePrimaryKey('list_id', 'book_id')
    list = models.ForeignKey('Lists', models.DO_NOTHING)
    book = models.ForeignKey(BookDetails, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'list_books'
        unique_together = (('list', 'book'),)


class ListTypes(models.Model):
    list_type_id = models.IntegerField(primary_key=True)
    type_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'list_types'


class Lists(models.Model):
    list_id = models.IntegerField(primary_key=True)
    list_name = models.TextField(blank=True, null=True)
    list_type = models.ForeignKey(ListTypes, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lists'


class NytBestsellers(models.Model):
    nyt_bestsellers_id = models.IntegerField(primary_key=True)
    book = models.ForeignKey(BookDetails, models.DO_NOTHING)
    date_nyt = models.DateField()
    ranking = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nyt_bestsellers'


class Review(models.Model):
    review_id = models.IntegerField(primary_key=True)
    book = models.ForeignKey(BookDetails, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    review_text = models.TextField(blank=True, null=True)
    created_at = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review'


class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.TextField(unique=True)
    password = models.TextField(blank=True, null=True)
    email = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'users'
