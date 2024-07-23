from django.contrib import admin
from .models import Mzalendo
# Register your models here.

class MzalendoAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", "age")}
    list_display = ('name', 'gender', 'county', 'age', 'life', 'dod', 'author', 'cover', 'date_created', 'updated_by', 'slug', 'updated_at', 'approved')

admin.site.register(Mzalendo, MzalendoAdmin)
