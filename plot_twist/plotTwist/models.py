from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BookDetails(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    pages = models.IntegerField(null=True, blank=True)
    date_published = models.CharField(max_length=20, null=True, blank=True)
    average_rating = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'book_details'
        managed = True

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
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)

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
    book = models.ForeignKey(BookDetails, db_column='book_id', on_delete=models.DO_NOTHING)
    # book = models.ForeignKey(BookDetails, models.DO_NOTHING, blank=True, null=True)
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
