from django.contrib import admin
from .models import Uzduotis


# Register your models here.
class UzduotisAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'vartotojas', 'sukurta', 'status')
    list_filter = ('status', 'vartotojas')



admin.site.register(Uzduotis, UzduotisAdmin)
