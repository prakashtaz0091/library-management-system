from django.db import models
from django.contrib.auth.models import User
import datetime







class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    is_librarian = models.BooleanField(default=False)
    mobile_number = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #if multiple roles
    #roles = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.user.username



class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    c_class = models.CharField(max_length=100)
    stock = models.IntegerField()

    category_choices = [
        ('Information Technology', 'Information Technology'),
        ('Science', 'Science'),
        ('General', 'General'),
        ('Social Science', 'Social Science'),
        ('Arts', 'Arts'),
        ('Literature', 'Literature'),
        ('Physcology', 'Physcology'),
        ('Management', 'Management'),
        ('Economy', 'Economy'),
    ]

    category = models.CharField(max_length=100, choices=category_choices)
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.name + ' by ' + self.author
    

    @classmethod
    def get_categories(cls):
        return [category for category, _ in cls.category_choices]

    #custom method



class Book_ISBN(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='isbns')
    created_at = models.DateTimeField(auto_now_add=True)
    issued = models.BooleanField(default=False)


    def __str__(self):
        return self.book.name + ' | ISBN: ' + str(self.id)
    



class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='checkouts')
    book_isbn = models.ForeignKey(Book_ISBN, on_delete=models.DO_NOTHING, null=True, related_name='checkouts')
    issued_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='checkouts_done', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(blank=True, null=True)


    def set_expiry_date(self):
        # self.expiry_date = self.created_at + datetime.timedelta(days=14)
        return None


    def set_issued_by(self, user):
        self.issued_by = user


    def __str__(self):
        return self.book.name + ' - ' + self.user.username
    

    def save(self, *args, **kwargs):
        self.set_expiry_date()

        self.set_issued_by(kwargs.pop('librarian', None))

        super(Checkout, self).save(*args, **kwargs)



class BookRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='book_requests')
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING , related_name='requests')
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' requested ' + self.book.name