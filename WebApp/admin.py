from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Album)
admin.site.register(Artist)
admin.site.register(Track)
admin.site.register(Popularity)
admin.site.register(Genre)
admin.site.register(Country)
