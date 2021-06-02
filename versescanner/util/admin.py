from django.contrib import admin

from .models.metadata import Author, Book, Genre, Opus, Period, Poem

# currently no need for admin classes
admin.site.register(Period)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Opus)
admin.site.register(Book)
admin.site.register(Poem)
