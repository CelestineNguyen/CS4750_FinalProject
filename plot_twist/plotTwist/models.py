# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Author(models.Model):
    author_id = models.IntegerField(primary_key=True)
    author_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'author'


class BookAuthor(models.Model):
    pk = models.CompositePrimaryKey('book_id', 'author_id')
    book = models.ForeignKey('Books', models.DO_NOTHING)
    author = models.ForeignKey(Author, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'book_author'
        unique_together = (('book', 'author'),)


class Books(models.Model):
    book_id = models.IntegerField(primary_key=True)
    title = models.TextField()
    isbn = models.TextField(unique=True, blank=True, null=True)
    pages = models.IntegerField(blank=True, null=True)
    date_published = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    average_rating = models.FloatField(blank=True, null=True)
    cover_image = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'books'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ListBooks(models.Model):
    pk = models.CompositePrimaryKey('list_id', 'book_id')
    list = models.ForeignKey('Lists', models.DO_NOTHING)
    book = models.ForeignKey(Books, models.DO_NOTHING)

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
    book = models.ForeignKey(Books, models.DO_NOTHING)
    date_nyt = models.DateField()
    ranking = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nyt_bestsellers'


class Review(models.Model):
    review_id = models.IntegerField(primary_key=True)
    book = models.ForeignKey(Books, models.DO_NOTHING, blank=True, null=True)
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

