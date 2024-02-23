from django.contrib import admin
from .models import Item, Swap, Profile

# Register your models here.
admin.site.register(Item)
admin.site.register(Swap)
admin.site.register(Profile)