from django.contrib import admin

# Register your models here.
from menu_app.models import Menu, MenuItem


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    model = Menu


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    model = MenuItem
